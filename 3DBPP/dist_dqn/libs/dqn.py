import os, os.path
import random
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import itertools
import tensorflow as tf
from collections import deque
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, concatenate, Conv2D, MaxPooling2D
#config = tf.compat.v1.ConfigProto(device_count={'GPU':1})
#sess = tf.compat.v1.Session(config=config) 
# CUDA_VISIBLE_DEVICES=""

class DQN_CNNDNN(tf.keras.Model):
    def __init__(self, state_size, selected_size, remain_size, loading_size, cbm_size,  w_size, output_size):
        super(DQN_CNNDNN, self).__init__()
        self.case_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = state_size) #filters=5,
        self.case_dnn1 = Dense(32, activation='relu')
        # location - selected boxes 
        self.sel_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = selected_size) #filters=5,
        self.sel_dnn1 = Dense(32, activation='relu')
        # size - remain boxes
        self.r_cnn1 = Conv2D(filters=32, kernel_size=3, activation='relu', padding="valid", input_shape = remain_size ) #filters=8,
        self.r_dnn1 = Dense(64, activation='relu')
        # size - selected boxes
        self.l_cnn1 = Conv2D(filters=8, kernel_size=(1,3), activation='relu', padding="valid", input_shape = loading_size ) #filters=3, 
        self.l_dnn1 = Dense(32, activation='relu')
        # cbm
        self.cbm_dnn1 = Dense(128, activation='relu', input_shape = cbm_size )
        self.cbm_dnn2 = Dense(32, activation='relu')
        # weight
        self.w_dnn1 = Dense(128, activation='relu', input_shape = w_size ) #64, 
        self.w_dnn2 = Dense(32, activation='relu')
        # all
        #n_ch = state_size[-1] + selected_size[-1] + remain_size[-1] + loading_size[-1] 
        #self.a_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid", input_shape = state_size[:-1]+(n_ch,))
        #self.a_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid")
        #self.a_dnn1 = Dense(32, activation='relu')
        # merge 
        self.fc1 = Dense(256, activation='relu')
        self.fc2 = Dense(128, activation='relu')
        if output_size > 1: #DDQN
            self.fc_out = Dense(output_size, activation='softmax')
        else:
            self.fc_out = Dense(output_size)

    def call(self, cb_list):
        c, s, r,l, cbm, w = cb_list[0], cb_list[1], cb_list[2], cb_list[3], cb_list[4], cb_list[5]
        #c, s, r = cb_list[0], cb_list[1], cb_list[2]
        ### case
        c = self.case_cnn1(c)
        c = MaxPooling2D(pool_size=(2, 2))(c)
        c = Flatten()(c)
        c = self.case_dnn1(c)
        ### location - selected boxes
        s = self.sel_cnn1(s)
        s = MaxPooling2D(pool_size=(2, 2))(s)
        s = Flatten()(s)
        s = self.sel_dnn1(s)
        ### size - remain boxes
        r = self.r_cnn1(r)
        r = MaxPooling2D(pool_size=(2, 2))(r)
        r = Flatten()(r)
        r = self.r_dnn1(r)
        ### size - selected boxes
        l = self.l_cnn1(l) #(32, 1, 60, 5)
        l = MaxPooling2D(pool_size=(1, 2))(l)#l = MaxPooling2D(pool_size=(2, 2))(l)
        l = Flatten()(l)
        l = self.l_dnn1(l)
        ### cbm
        cbm = self.cbm_dnn1(cbm)
        cbm = self.cbm_dnn2(cbm)
        ### weight
        w = self.w_dnn1(w)
        w = self.w_dnn2(w)
        ### all
        #a =  tf.concat([c, r, l], -1)
        #a = self.a_cnn1(a)
        #a = MaxPooling2D(pool_size=(2, 2))(a)
        #a = Flatten()(a)
        #a = self.a_dnn1(a)
        ### merge
        x = concatenate([c,s,r,l, cbm, w])
        x = self.fc1(x)
        x = self.fc2(x)
        q = self.fc_out(x)
        return q    

class DQNAgent:
    def __init__(self, L=20, B=20, H=20, n_remains = 5, n_loading=3, n_channel = 4, max_size = 64,
                 lr=1e-8, batch_size = 32, exp_steps=500, train_st = 200, memory_len=500, update_target_rate = 30, net='DNN' ):
        self.state_size = (L, B, 4) # 합, 높이, 대박스 규격, 무게
        self.selected_size = (L, B, n_loading*2) #적입할 중박스의 위치와 무게
        self.remain_size = (n_remains, max_size ,n_channel) # 남은 중박스 규격(세로가로), 적입된 중박스 규격(세로가로)
        self.loading_size = (n_loading, max_size ,n_channel//2) # 적입할 중박스 규격(세로가로)
        self.cbm_size = (1 + n_remains*2 + n_loading,) #대박스 CBM, 남은 중박스 CBM, 적입된 중박스 CBM, 적입할 중박스 CBM 
        self.w_size = (n_remains + n_loading + 8,) # 남은 중박스 무게, 적입할 중박스 무게
        self.output_size = 1 # DQN output (dist 아님)
        # hyperparameters
        self.discount_factor = 0.99
        self.learning_rate = lr#1e-8#1e-4
        self.epsilon = 1.
        self.epsilon_start, self.epsilon_end = 1.0, 0.01
        self.exploration_steps = exp_steps
        self.epsilon_decay_step = self.epsilon_start - self.epsilon_end
        self.epsilon_decay_step /= self.exploration_steps
        self.batch_size = batch_size
        self.train_start = train_st
        self.update_target_rate = update_target_rate
        self.beta = 0.2
        self.memory = deque(maxlen=memory_len) # replay memory
        self.net = net
        self.vmin = 0#-0.02
        self.vmax = 1
        self.nsup = 51#52
        self.dz = (self.vmax - self.vmin)/(self.nsup - 1.)
        self.z = np.linspace(self.vmin,self.vmax,self.nsup)
        self.gamma = 0.9
        self.criterion = tf.keras.losses.CategoricalCrossentropy()
        self.dist = False
        # model
        if net == 'DNN':
            self.model = DQN_DNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
            self.target_model = DQN_DNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
        elif net =='CNN':
            self.model = DQN_CNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
            self.target_model = DQN_CNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
        elif net =='CNNDNN':
            self.model = DQN_CNNDNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
            self.target_model = DQN_CNNDNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
        # distributed q learning
        elif net == 'DDQN_DNN':
            self.model = DQN_DNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.cbm_size, self.nsup)
            self.target_model = DQN_DNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.cbm_size, self.nsup)
        elif net == 'DDQN_CNNDNN':
            self.model = DQN_CNNDNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.cbm_size, self.w_size, self.nsup)
            self.target_model = DQN_CNNDNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.cbm_size, self.w_size, self.nsup)
        
        if net in ['DDQN_DNN', 'DDQN_CNNDNN']:
            print('distribution', net)
            self.dist = True
        
        self.optimizer = Adam(self.learning_rate)#, clipnorm=10.)
        # target model (init)
        self.update_target_model()
        self.avg_q_max, self.avg_loss = 0, 0
#         self.writer = tf.summary.create_file_writer('summary/bpp')
        self.model_path = os.path.join(os.getcwd(), 'save_model', 'model_3d')

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def get_action(self, state, loaded_mh_c, r_boxes, loading, cbm, w):
        if np.random.rand() <= self.epsilon:
            random_action = random.randrange(len(state))
            return random_action
        else:
            if self.dist:
                z = self.model.predict([state, loaded_mh_c, r_boxes, loading, cbm, w]) #(C,51)
                z_concat = np.vstack(z) #action output이 여러개 일때
                #q = np.sum(np.multiply(z_concat[:,45:], np.array(self.z)[45:]), axis=1) #(C,)
                q = np.sum(np.multiply(z_concat, np.array(self.z)), axis=1) #(C,)
                self.avg_q_max += np.amax(q)
                return np.argmax(q)
            else:
                q_values=self.model([state, loaded_mh_c, r_boxes, loading, cbm, w])
                armax_idx = np.where( q_values == tf.math.reduce_max(q_values))
                action_idx = armax_idx[0][0]
                return action_idx
    
   
    def append_sample(self, history, load, remain_size, load_size, reward, last, t_history, t_load, t_remain_size, t_load_size, cbm,  t_cbm, w, t_w):
        self.memory.append(( history, load, remain_size, load_size, reward, last, t_history, t_load, t_remain_size, t_load_size, cbm, t_cbm, w, t_w))
        
        
#     def draw_tensorboard(self, reward, fill, step, episode):
#         with self.writer.as_default():
#             tf.summary.scalar('Total Reward/Episode', reward, step=episode)
#             tf.summary.scalar('Total Fill/Episode', fill, step=episode)
#             tf.summary.scalar('Average Max Q/Episode', self.avg_q_max / float(step), step=episode)
#             tf.summary.scalar('Duration/Episode', step, step=episode)
#             tf.summary.scalar('Average Loss/Episode', self.avg_loss / float(step), step=episode)
    
    def train_model(self):
        
        batch = random.sample(self.memory, self.batch_size)
        
        history = np.array([sample[0] for sample in batch])# (B, 20,20,2)
        load = np.array([sample[1] for sample in batch])# (B, 20,20,1)
        remain_size = np.array([sample[2] for sample in batch]) # (B, 20,20, max_num_remain)
        load_size = np.array([sample[3] for sample in batch]) # (B, 20, 20, K)
        reward = np.array([sample[4] for sample in batch]) # (B,)
        dones = np.array([sample[5] for sample in batch]) # (B,)
        len_t_comb = [ len(sample[6]) for sample in batch ]
        t_history = np.concatenate([sample[6] for sample in batch] )
        t_load = np.concatenate([sample[7] for sample in batch])
        t_remain_size = np.concatenate([sample[8] for sample in batch] )
        t_load_size = np.concatenate([sample[9] for sample in batch] )
        cbm = np.array([sample[10] for sample in batch] )
        t_cbm = np.concatenate([sample[11] for sample in batch] )
        w = np.array([sample[12] for sample in batch] )
        t_w = np.concatenate([sample[13] for sample in batch] )
        
        #print(history.shape,load.shape,remain_size.shape, load_size.shape, reward.shape, dones.shape,  t_history.shape, t_load.shape, t_remain_size.shape, t_load_size.shape)
        
        model_params = self.model.trainable_variables
        with tf.GradientTape() as tape:
            if self.dist:
                # 예측
                predicts = self.model([history, load, remain_size, load_size, cbm, w]) # B,51
                # 타겟
#                 z_b = []
#                 for i in range(0,len(t_history), self.batch_size):
#                     e_idx = min( i + self.batch_size, len(t_history) )
#                     z = self.target_model([t_history[i:e_idx], t_load[i:e_idx], t_remain_size[i:e_idx], t_load_size[i:e_idx]]) #(C, 51)
#                     z_b.append(z)
#                 z_concat = np.vstack(z_b) #(B*c, 51)
                z_concat = self.target_model([t_history, t_load, t_remain_size, t_load_size, t_cbm, t_w])
                t_q = np.sum(np.multiply(z_concat, np.array(self.z)), axis=1) #(B*c, )
                # 가장 기댓값이 높은 action 선택
                next_actions, probs = [],[]
                for i in range(len(len_t_comb)):
                    s_idx = np.sum(len_t_comb[:i]).astype('int')
                    if len_t_comb[i] ==1:
                        n_a = 0
                    else:                        
                        n_a = np.argmax(t_q[s_idx: s_idx + len_t_comb[i]])
                    next_actions.append(n_a) #[32]
                    probs.append((z_concat[s_idx: s_idx + len_t_comb[i]])[n_a])
                probs = np.stack(probs) #(B, 51)
                # target distribution
                bj = np.round((reward - self.vmin)/self.dz) #(B,)
                #지지 성분의 색인
                bj = np.clip(bj, 0, self.nsup-1).astype('int') #유효한 범위
                targets = []
                for i in range(self.batch_size):
                    if dones[i]:
                        target_dist = np.zeros(self.nsup)
                        target_dist[bj[i]] = 1
                        targets.append(target_dist)
                    else:
                        m = probs[i].copy() #(51,)
                        j = 1
                        for i in range(bj[i],1,-1):
                            m[i] += np.power(self.gamma, j) * m[i-1]
                            j += 1
                        j = 1
                        for i in range(bj[i], self.nsup-1,1):
                            m[i] += np.power(self.gamma, j) * m[i+1]
                            j += 1
                        m /= m.sum() #(51,)
                        targets.append(m)
                loss = self.criterion(targets, predicts)
            else: 
                # 예측
                predicts = self.model([history, load, remain_size, load_size]) #(B, 1)
                # 타겟
                targets = []
                for i in range(self.batch_size):
                    t_q = self.target_model([t_history[i], t_load[i], t_remain_size[i], t_load_size[i], t_cbm[i], t_w[i]]) # target q value
                    t_max_q = tf.math.reduce_max(t_q)
                    targets.append([(1- 0.75)*reward[i] + (1 - dones[i]) *0.75*t_max_q])
                targets=np.array(targets) #(B, 1)
                # loss 계산
                #loss = tf.reduce_mean(tf.square(targets - predicts))
                error = tf.abs(targets - predicts)
                quadratic_part = tf.clip_by_value(error, 0.0, 1.0)
                linear_part = error - quadratic_part
                loss = tf.reduce_mean(0.5 * tf.square(quadratic_part) + linear_part)
            
            self.avg_loss += loss.numpy()
            
        # update
        grads = tape.gradient(loss, model_params)
        self.optimizer.apply_gradients(zip(grads, model_params))
    


    
    
    
