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
    def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
        super(DQN_CNNDNN, self).__init__()
        self.case_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid", input_shape = state_size)
        self.case_dnn1 = Dense(32, activation='relu')
        # location - selected boxes
        self.sel_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid", input_shape = selected_size)
        self.sel_dnn1 = Dense(32, activation='relu')
        # remain boxes
        self.r_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid", input_shape = remain_size )
        self.r_dnn1 = Dense(64, activation='relu')
        # all
        #n_ch = state_size[-1] + selected_size[-1] + remain_size[-1] + loading_size[-1] 
        #self.a_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid", input_shape = state_size[:-1]+(n_ch,))
        #self.a_dnn1 = Dense(32, activation='relu')
        # merge 
        self.fc1 = Dense(256, activation='relu')
        self.fc2 = Dense(128, activation='relu')
        if output_size > 1: #DDQN
            self.fc_out = Dense(output_size, activation='softmax')
        else:
            self.fc_out = Dense(output_size)

    def call(self, cb_list):
        c, s, r = cb_list[0], cb_list[1], cb_list[2]
        #a =  tf.concat([c, s, r], -1)
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
        ### remain boxes
        r = self.r_cnn1(r)
        r = MaxPooling2D(pool_size=(2, 2))(r)
        r = Flatten()(r)
        r = self.r_dnn1(r)
        ### all
        #a = self.a_cnn1(a)
        #a = MaxPooling2D(pool_size=(2, 2))(a)
        #a = Flatten()(a)
        #a = self.a_dnn1(a)
        ### merge
        x = concatenate([c,s,r])#x = concatenate([c,s,r,a])
        x = self.fc1(x)
        x = self.fc2(x)
        q = self.fc_out(x)
        return q

# class DQN_CNN(tf.keras.Model):
#     def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
#         super(DQN_CNN, self).__init__()
#         self.case_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = state_size)
#         #self.case_cnn2 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid")
        
#         # location - selected boxes
#         self.sel_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = selected_size)
#         #self.sel_cnn2 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid")
        
#         # remain boxes
#         self.r_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = remain_size )
#         #self.r_cnn2 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid")
        
#         # all
#         n_ch = state_size[-1] + selected_size[-1] + remain_size[-1] + loading_size[-1] 
#         self.a_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = state_size[:-1]+(n_ch,))
        
#         # merge 
#         self.fc1 = Dense(256, activation='relu')
#         self.fc2 = Dense(128, activation='relu')
#         self.fc_out = Dense(output_size)

#     def call(self, cb_list):
#         c, s, r = cb_list[0], cb_list[1], cb_list[2]
#         a =  tf.concat([c, s, r], -1)
#         ### case
#         c = self.case_cnn1(c)
#         c = MaxPooling2D(pool_size=(2, 2))(c)
#         #c = self.case_cnn2(c)
#         #c = MaxPooling2D(pool_size=(2, 2))(c)
#         c = Flatten()(c)
        
#         ### location - selected boxes
#         s = self.sel_cnn1(s)
#         s = MaxPooling2D(pool_size=(2, 2))(s)
#         #s = self.sel_cnn2(s)
#         #s = MaxPooling2D(pool_size=(2, 2))(s)
#         s = Flatten()(s)
        
#         ### remain boxes
#         r = self.r_cnn1(r)
#         r = MaxPooling2D(pool_size=(2, 2))(r)
#         #r = self.r_cnn2(r)
#         #r = MaxPooling2D(pool_size=(2, 2))(r)
#         r = Flatten()(r)
        
#         ### all
#         a = self.a_cnn1(a)
#         a = MaxPooling2D(pool_size=(2, 2))(a)
#         a = Flatten()(a)
        
#         ### merge
#         x = concatenate([c,s,r,l,a])
#         x = self.fc1(x)
#         x = self.fc2(x)
#         q = self.fc_out(x)
#         return q


# class DQN_CNN(tf.keras.Model):
#     def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
#         super(DQN_CNN, self).__init__()
#         # all
#         n_ch = state_size[-1] + selected_size[-1] + remain_size[-1] #+ loading_size[-1] 
#         self.a_cnn1 = Conv2D(filters=32, kernel_size=3, activation='relu', padding="valid", input_shape = state_size[:-1]+(n_ch,))
#         self.a_cnn2 = Conv2D(filters=32, kernel_size=3, activation='relu', padding="valid")
#         self.a_cnn2 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid")
#         # merge 
#         self.fc1 = Dense(256, activation='relu')
#         self.fc2 = Dense(128, activation='relu')
#         self.fc_out = Dense(output_size)

#     def call(self, cb_list):
#         c, s, r = cb_list[0], cb_list[1], cb_list[2]
#         a =  tf.concat([c, s, r], -1)
#         ### all
#         a = self.a_cnn1(a)
#         a = MaxPooling2D(pool_size=(2, 2))(a)
#         a = self.a_cnn2(a)
#         a = MaxPooling2D(pool_size=(2, 2))(a)
#         x = Flatten()(a)
#         ### merge
#         x = self.fc1(x)
#         x = self.fc2(x)
#         q = self.fc_out(x)
#         return q
    
    
class DQN(tf.keras.Model):
    def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
        super(DQN, self).__init__()
        # case network
        l1,b1,k1 = state_size # 배치 사이즈 제외된 사이즈
        self.state_size = (l1*b1*k1,)
        self.case_dnn1 = Dense(64, activation='tanh',input_shape = self.state_size)
        self.case_dnn2 = Dense(64, activation='tanh')#
        # location - selected boxes
        l2,b2,k2 = selected_size
        self.selected_size = (l2*b2*k2,)
        self.sel_dnn1 = Dense(64, activation='tanh',input_shape = self.selected_size)
        self.sel_dnn2 = Dense(64, activation='tanh')#
        # remain boxes
        l3,b3,k3 = remain_size
        self.remain_size = (l3*b3*k3, )
        self.r_dnn1 = Dense(128, activation='tanh', input_shape = self.remain_size  )
        self.r_dnn2 = Dense(128, activation='tanh')
        # all
        #self.all_size = (self.state_size[0]+self.selected_size[0]+self.remain_size[0]+self.loading_size[0], )
        #self.a_dnn1 = Dense(128, activation='relu', input_shape = self.all_size  )
        # merge 
        self.fc1 = Dense(256, activation='tanh')
        self.fc2 = Dense(256, activation='tanh')
        self.fc2 = Dense(128, activation='tanh')
        self.fc_out = Dense(output_size)

    def call(self, cb_list):
        c, s, r = cb_list[0], cb_list[1], cb_list[2]
        c = tf.reshape(c, [-1, self.state_size[0]])
        s = tf.reshape(s, [-1, self.selected_size[0]])
        r = tf.reshape(r, [-1, self.remain_size[0]])
        #a =  tf.concat([c, s, r, l], -1)
        ### case
        c = self.case_dnn1(c)
        c = self.case_dnn2(c)
        ### location - selected boxes
        s = self.sel_dnn1(s)
        s = self.sel_dnn2(s)
        ### remain boxes
        r = self.r_dnn1(r)
        r = self.r_dnn2(r)
        ### all
        #a = self.a_dnn1(a)
        ### merge
        x = concatenate([c,s,r])#x = concatenate([c,s,r,l,a])
        x = self.fc1(x)
        x = self.fc2(x)
        q = self.fc_out(x)
        return q

class DDQN(tf.keras.Model):
    def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
        super(DDQN, self).__init__()
        # case network
        l1,b1,k1 = state_size # 배치 사이즈 제외된 사이즈
        self.state_size = (l1*b1*k1,)
        self.case_dnn1 = Dense(64, activation='relu',input_shape = self.state_size)
        self.case_dnn2 = Dense(64, activation='relu')#
        # location - selected boxes
        l2,b2,k2 = selected_size
        self.selected_size = (l2*b2*k2,)
        self.sel_dnn1 = Dense(64, activation='relu',input_shape = self.selected_size)
        self.sel_dnn2 = Dense(64, activation='relu')#
        # remain boxes
        l3,b3,k3 = remain_size
        self.remain_size = (l3*b3*k3, )
        self.r_dnn1 = Dense(128, activation='relu', input_shape = self.remain_size  )
        self.r_dnn2 = Dense(128, activation='relu')
        # all
        #self.all_size = (self.state_size[0]+self.selected_size[0]+self.remain_size[0]+self.loading_size[0], )
        #self.a_dnn1 = Dense(128, activation='relu', input_shape = self.all_size  )
        # merge 
        self.fc1 = Dense(256, activation='relu')
        self.fc2 = Dense(256, activation='relu')
        self.fc2 = Dense(128, activation='relu')
        self.fc_out = Dense(output_size, activation='softmax')

    def call(self, cb_list):
        c, s, r = cb_list[0], cb_list[1], cb_list[2]
        c = tf.reshape(c, [-1, self.state_size[0]])
        s = tf.reshape(s, [-1, self.selected_size[0]])
        r = tf.reshape(r, [-1, self.remain_size[0]])
        #a =  tf.concat([c, s, r, l], -1)
        ### case
        c = self.case_dnn1(c)
        c = self.case_dnn2(c)
        ### location - selected boxes
        s = self.sel_dnn1(s)
        s = self.sel_dnn2(s)
        ### remain boxes
        r = self.r_dnn1(r)
        r = self.r_dnn2(r)
        ### all
        #a = self.a_dnn1(a)
        ### merge
        x = concatenate([c,s,r])#x = concatenate([c,s,r,l,a])
        x = self.fc1(x)
        x = self.fc2(x)
        q = self.fc_out(x)
        return q


class DQNAgent:
    def __init__(self, L=20, B=20, H=20, n_remains = 5, n_loading=3, lr=1e-8, 
                 exp_steps=500, train_st = 200, memory_len=500, update_target_rate = 30, net='DNN' ):
        self.state_size = (L, B, 1)
        self.selected_size = (L, B, 2)
        self.remain_size = (L, B, n_remains)
        self.loading_size = (L, B, n_loading)
        self.output_size = 1 #math.factorial(c_boxes_size)
        # hyperparameters
        self.discount_factor = 0.99
        self.learning_rate = lr#1e-8#1e-4
        self.epsilon = 1.
        self.epsilon_start, self.epsilon_end = 1.0, 0.01
        self.exploration_steps = exp_steps
        self.epsilon_decay_step = self.epsilon_start - self.epsilon_end
        self.epsilon_decay_step /= self.exploration_steps
        self.batch_size = 32
        self.train_start = train_st
        self.update_target_rate = update_target_rate
        self.beta = 0.2
        self.memory = deque(maxlen=memory_len) # replay memory
        self.net = net
        self.vmin = 0
        self.vmax = 1
        self.nsup = 51
        self.dz = (self.vmax - self.vmin)/(self.nsup - 1.)
        self.z = np.linspace(self.vmin,self.vmax,self.nsup)
        self.gamma = 0.9
        self.criterion = tf.keras.losses.CategoricalCrossentropy()
        self.dist = False
        # model
        if net == 'DNN':
            self.model = DQN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
            self.target_model = DQN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
        elif net =='CNN':
            self.model = DQN_CNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
            self.target_model = DQN_CNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
        elif net =='CNNDNN':
            self.model = DQN_CNNDNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
            self.target_model = DQN_CNNDNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.output_size)
        elif net == 'DDQN':
            self.model = DDQN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.nsup)
            self.target_model = DDQN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.nsup)
        elif net == 'DDQN_CNNDNN':
            self.model = DQN_CNNDNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.nsup)
            self.target_model = DQN_CNNDNN(self.state_size, self.selected_size, self.remain_size, self.loading_size, self.nsup)
        
        if net in ['DDQN', 'DDQN_CNNDNN']:
            print('distribution', net)
            self.dist = True
        
        self.optimizer = Adam(self.learning_rate)#, clipnorm=10.)
        # target model (init)
        self.update_target_model()
        self.avg_q_max, self.avg_loss = 0, 0
        self.writer = tf.summary.create_file_writer('summary')
        self.model_path = os.path.join(os.getcwd(), 'save_model', 'model_3d')

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def get_action(self, state, loaded_mh_c, r_boxes, loading):
        if np.random.rand() <= self.epsilon:
            random_action = random.randrange(len(state))
            return random_action
        else:
            if self.dist:
                z = self.model.predict([state, loaded_mh_c, r_boxes, loading]) #(C,51)
                z_concat = np.vstack(z) #action output이 여러개 일때
                q = np.sum(np.multiply(z_concat, np.array(self.z)), axis=1) #(C,)
                return np.argmax(q)
            else:
                q_values=self.model([state, loaded_mh_c, r_boxes, loading])
                armax_idx = np.where( q_values == tf.math.reduce_max(q_values))
                action_idx = armax_idx[0][0]
                return action_idx
    
   
    def append_sample(self, history, load, remain_size, load_size, reward, last, t_history, t_load, t_remain_size, t_load_size):
        self.memory.append(( history, load, remain_size, load_size, reward, last, t_history, t_load, t_remain_size, t_load_size))
        
        
    # 텐서보드에 학습 정보를 기록
    #def draw_tensorboard(self, score, step, episode):
    #    with self.writer.as_default():
    #        tf.summary.scalar('Total Reward/Episode', score, step=episode)
    #        tf.summary.scalar('Average Max Q/Episode',
    #                          self.avg_q_max / float(step), step=episode)
    #        tf.summary.scalar('Duration/Episode', step, step=episode)
    #        tf.summary.scalar('Average Loss/Episode',
    #                          self.avg_loss / float(step), step=episode)
    
    def train_model(self):
        
        batch = random.sample(self.memory, self.batch_size)
        
        history = np.array([sample[0] for sample in batch])# (B, 20,20,1)
        load = np.array([sample[1] for sample in batch])# (B, 20,20,2)
        remain_size = np.array([sample[2] for sample in batch]) # (B, 20,20, max_num_remain)
        load_size = np.array([sample[3] for sample in batch]) # (B, 20, 20, K)
        reward = np.array([sample[4] for sample in batch]) # (B,)
        dones = np.array([sample[5] for sample in batch]) # (B,)
        t_history = [sample[6] for sample in batch] 
        t_load = [sample[7] for sample in batch]
        t_remain_size = [sample[8] for sample in batch] 
        t_load_size = [sample[9] for sample in batch] 
        
        model_params = self.model.trainable_variables
        with tf.GradientTape() as tape:
            if self.dist:
                # 예측
                predicts = self.model([history, load, remain_size, load_size]) # B,51
                # 타겟
                targets = []
                for i in range(self.batch_size):
                    z = self.target_model([t_history[i], t_load[i], t_remain_size[i], t_load_size[i]]) #(C, 51)
                    z_concat = np.vstack(z) #(C, 51), (51,)
                    t_q = np.sum(np.multiply(z_concat, np.array(self.z)), axis=1) #(C, )
                    next_actions = np.argmax(t_q)
                    probs = z_concat[next_actions] #(51,)
                    # target distribution
                    bj = np.round((reward[i] - self.vmin)/self.dz) #지지 성분의 색인
                    bj = int(np.clip(bj, 0, self.nsup-1)) #유효한 범위
                    if dones[i]:
                        target_dist = np.zeros(self.nsup)
                        target_dist[bj] = 1
                        targets.append(target_dist)
                    else:
                        m = probs.copy()
                        j = 1
                        for i in range(bj,1,-1):
                            m[i] += np.power(self.gamma, j) * m[i-1]
                            j += 1
                        j = 1
                        for i in range(bj, self.nsup-1,1):
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
                    t_q = self.target_model([t_history[i], t_load[i], t_remain_size[i], t_load_size[i]]) # target q value
                    t_max_q = tf.math.reduce_max(t_q)
                    targets.append([(1- 0.75)*reward[i] + (1 - dones[i]) *0.75*t_max_q])
                #t_q = []
                #for i in range(len(t_history)):
                #    st = (self.batch_size)*(i)
                #    ed = min((self.batch_size)*(i+1), len(t_history) )
                #    if ed >= len(t_history):
                #        t_q.append( self.target_model([t_history[st:], t_s_boxes[st:], t_remains[st:]]) )
                #        break
                #    t_q.append( self.target_model([t_history[st:ed], t_s_boxes[st:ed], t_remains[st:ed]]) )
                #t_q = tf.concat(t_q, 0)
                ##t_q = self.target_model([t_history, t_s_boxes, t_remains]) # target q value
                #st = 0
                #for i,l in enumerate(t_len):
                #    t_max_q = tf.math.reduce_max(t_q[st:st+l])
                #    targets.append([(1- 0.75)*reward[i] + (1 - dones[i]) *0.75*t_max_q])
                #    st = st+l

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
    


    
    
    
