import os, os.path
os.environ["CUDA_VISIBLE_DEVICES"]=""
# tf_device='/gpu:0'
import argparse
is_pred = True 

# python -u mlp_single_hyper.py --mi GA --mbox_type PP | tee log/predict.txt;

parser = argparse.ArgumentParser()
parser.add_argument('--mi')
parser.add_argument('--mbox_type')
args = parser.parse_args()
args = args.__dict__
training_setting = {
    'lr':1e-4,
    'exp_steps':19000,
    'train_st':300,
    'memory_len':300,
    'update_target_rate':150,
    'net':'DDQN_CNNDNN',
    'batch_size': 32
}
args.update(training_setting)

num_episode = 20000
global_step = 0
tr_l, h_fill, tr_r,avg_loss_l,history_eps,used_boxes_eps  = [],[],[],[],[],[]
max_k = 1
K = 1
n_candidates = 100
num_max_remain = 128
n_channel = 4 # (남은 중박스의 가로, 남은 중박스의 세로, 적입된 중박스의 가로, 적입된 중박스의 세로)

mi = args['mi']  #'GA'
mbox_type = args['mbox_type'] #'PP'
f_name =  'plan_predict_input/' + mi+'_'+mbox_type#'plan_input/' + mi+'_'+mbox_type #
path_preprocessed = 'data/preprocessed/'
path_df_bbox = 'data/preprocessed/bbox/'
path_save_model = 'save_model/'
print(mi, mbox_type)
######################################################################################################################################
import random
import pickle
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import tensorflow as tf
tf.get_logger().setLevel('INFO')
tf.keras.backend.floatx()
from collections import deque
import itertools
from sklearn.utils import shuffle
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense
from libs.utils import *
from libs.generate_boxes import *
from libs.dqn import *

# scaling list
with open(path_preprocessed+'sc_list.pickle', 'rb') as handle: 
    sc_list =  pickle.load(handle) #cbm_mx, weight_mx, mbox_h_mx
sc_list =  sc_list[mi+'_'+mbox_type]   
with open(path_preprocessed + 'max_size_list.pickle', 'rb') as handle: 
    max_size_list =  pickle.load(handle) #cbm_mx, weight_mx, mbox_h_mx
max_size =  max_size_list[mi+'_'+mbox_type]   

# 대박스 규격 로드
casemaster=pd.read_csv(path_preprocessed+'casemaster.csv')
df_bbox = pd.read_csv(path_df_bbox + mi + '_' + mbox_type + '.csv')
num_bbox_type = len(df_bbox)
df_bbox = df_bbox.iloc[:num_bbox_type]
df_bbox = df_bbox.drop(['CASE_CD_count'], axis=1)
# 대박스 규격 로드 (Env)
bbox_size = pd.read_csv(path_df_bbox + mi + '_' + mbox_type + '.csv')
bbox_size = bbox_size.values[:num_bbox_type, 1:4]
bbox_size = np.concatenate([np.sort(bbox_size[:,:2], axis=1), bbox_size[:,2:]], axis=-1) # 정렬
# 대박스 스케일링
sc = 1/20
bbox_sc = bbox_size.copy() 
bbox_sc[:, :2] = bbox_size[:,:2] * sc # 세로가로만 스케일링
bbox_sc = (bbox_sc).astype('int') #내림 #(bbox_sc+0.5).astype('int') #반올림
mxl, mxb, mxh = np.max(bbox_sc, axis =0 ) # 최대 규격
print(mxl, mxb, mxh)
# 대박스 행렬로 변환
bbox_type = [] #np.zeros((1, 20, 20))
for l,b,h in bbox_sc:
    bbox = np.zeros((mxl, mxb))
    bbox[l:,:] = mxh
    bbox[:,b:] = mxh
    bbox[:l,:b] = mxh - h
    bbox_type.append(bbox)
bbox_type = np.stack((bbox_type)) #(5, 20, 20)
# 대박스 CBM 스케일링
bbox_cbm_mx = np.max(df_bbox['CBM'])

# 중박스 데이터 로드 (data frame)
group_key = ['creat_dd', 'odr_no', 'ctmmny_cd', 'mbox_type']
resid = pd.read_csv(path_preprocessed + f_name + '_resid.csv')
org_col = resid.columns
resid = resid.sort_values('sum_wt', ascending = False)
resid = resid.set_index(group_key).sort_index()
group_idx = resid.index.drop_duplicates()
# 중박스 데이터 로드 (입력 데이터)
with open(path_preprocessed + f_name +'_resid.pickle', 'rb') as handle: 
    boxes_multi =  pickle.load(handle)
with open(path_preprocessed + f_name +'_resid_v0.pickle', 'rb') as handle: 
    boxes_multi_n =  pickle.load(handle)
# 중박스 정렬
boxes_multi = [ np.concatenate([np.sort(x[:, :2], axis=1), x[:, 2:]], axis=-1) for x in  boxes_multi]
boxes_multi_n = [ np.concatenate([np.sort(x[:, :2], axis=1), x[:, 2:]], axis=-1) for x in  boxes_multi_n]
# 중박스 크기 스케일링
boxes_multi_sc = [ np.concatenate([np.ceil(x[:, :2] * sc), x[:, 2:3]], axis=-1).astype('int') for x in  boxes_multi]
boxes_multi_n_sc = [ np.concatenate([np.ceil(x[:, :2] * sc), x[:, 2:6]], axis=-1) for x in  boxes_multi_n]
# CBM
cbm_bbox = df_bbox['CBM'].values # 대박스 CBM
cbm_bbox = (cbm_bbox - np.min(cbm_bbox)) / np.ptp(cbm_bbox) # 스케일링된 대박스 CBM
cbm_per_mbox = [x[:,-1] for x in boxes_multi] # 중박스 CBM
cbm_mx =  sc_list[0] #np.max(np.concatenate(cbm_per_mbox))
cbm_mbox = [ x/cbm_mx for x in cbm_per_mbox] # 스케일링된 중박스 CBM
# 무게
weight_mbox = [x[:,3]/(x[:,0]*x[:,1]) for x in boxes_multi] # 중박스 무게
weight_mx =  sc_list[1] # np.max(np.concatenate([x[:,3] for x in boxes_multi] ))
weight_mbox = [ x/weight_mx for x in weight_mbox] 
# 중박스 크기를 행렬로 표현 & 범위 스케일링
mbox_mat = [x.copy() for x in boxes_multi_n_sc] #.copy -> not working
mbox_h_mx = sc_list[2]#np.max(resid['M_H'])
for i in range(len(mbox_mat)): mbox_mat[i][:,2] = mbox_mat[i][:,2] /mbox_h_mx  
#max_size = np.max(np.concatenate(boxes_multi_sc)[:,:2]) 
max_size = (max_size* sc).astype('int')
df_num_max_remain = max(resid.groupby(group_key)['num_mbox'].agg('sum').astype('int'))
mbox_mat = np.stack([size2mat(x, max(df_num_max_remain, num_max_remain),max_size) for x in mbox_mat]) # (N, num_max_remain, max_size, 4)
mbox_mat = np.concatenate([mbox_mat, np.zeros_like(mbox_mat)], axis = -1) # 남은 박스 규격 + 적입된 박스 규격

# Environment
env = Bpp3DEnvMS(length = mxl, breadth = mxb, height = mxh, bbox_type = bbox_type)

# Agent
agent = DQNAgent( L = mxl, B = mxb , H = mxh, n_remains = num_max_remain, n_loading=K, n_channel = n_channel, max_size = max_size,
                 lr=args['lr'], batch_size = args['batch_size'], exp_steps=args['exp_steps'], train_st = args['train_st'], 
                 memory_len=args['memory_len'], update_target_rate = args['update_target_rate'], net = args['net']) #DDQN_CNNDNN
#######################################################################################################################################

tot_st = time.time()
loading_loc_shape = (mxl, mxb, K*2)

if is_pred:
    num_episode = len(boxes_multi_sc)
    pk = pd.DataFrame(columns = ['pack_no']+list(org_col)+['packing_rate_cbm','packing_rate_volume',
                                                           'x','y','z','M_L2','M_B2','P_bbox_cd','P_L','P_B','P_H','P_CBM']) # 예측 결과 테이블
    pack_no = 0
    agent.epsilon = 0
    #agent.model.load_weights('save_model/'+mi+'_'+mbox_type+'/model_'+mi+'_'+mbox_type)
    agent.model.load_weights(path_save_model+'model2_'+mi+'_'+mbox_type)

reward_w_l = []         
for e in range(num_episode): #
    st=time.time()
    step = 0
    ith_data = e
    # 중박스 그룹
    boxes_all_sc = boxes_multi_sc[ ith_data].copy().astype('int') # 스케일링된 중박스 규격 
    if np.sum(boxes_all_sc[:,:2] > np.max(bbox_sc[:,:2])): continue # 중박스 규격이 대박스 규격보다 큰 경우에 스킵
        
    if is_pred:
        df_p = resid.loc[group_idx[ith_data]].reset_index().copy()
        df_p = df_p.loc[df_p.index.repeat(df_p['num_mbox'])] # 각 행을 num_mbox번 만큼 반복
    else:
        #if e > 9000: agent.epsilon = 0
        if agent.epsilon > agent.epsilon_end and len(agent.memory)>=agent.train_start:
            agent.epsilon -= agent.epsilon_decay_step
    cbm_all = cbm_per_mbox[ith_data].copy() # 충진율 계산에 사용(스케일링 X, 업데이트 X)
    r_boxes = boxes_all_sc.copy() # 남은 중박스 규격 (초기화 ~> 업데이트)
    m_mat = mbox_mat[ith_data].copy() # 규격 행렬 (초기화 ~> 업데이트)
    w_mbox =  weight_mbox[ith_data].copy() # 남은 중박스 무게 (스케일링은 되어있음, 업데이트 X)
    boxes_idx = np.arange(len(boxes_all_sc)) # 남은 중박스 인덱스 (초기화)
    loaded_idx = [] # 적입된 중박스 인덱스
    used_boxes, pred_pos = [],[] # 사용된 중박스(방향 반영), 위치
    env_rewards, is_last, used_bbox = [], [], [] # cbm 충진율 보상, 각 대박스 적입 완료 여부, 사용된 대박스 
    env_rewards_w = [] # 무게 균형에 대한 보상
    history, h_load, h_remain_size, h_load_size, h_cbm, h_weight = [],[],[],[],[],[]
    t_history, t_load, t_remain_size, t_load_size, t_cbm, t_weight = [],[],[],[],[],[]
    reward_w  = []
    
    while len(r_boxes) > 0: #모든 중박스를 다 적입할 때까지 반복 (새로운 대박스 시작)
        done = False
        len_group = 0 #현재 대박스에 적입된 중박스 수
        cbm_reward = 0
        # state 선택
        mask = [ sum((i >= r_boxes[:n_candidates]).sum(1)==3)>=1 for i in bbox_sc] #적입 가능한 대박스중에서만 선택
        if sum(mask)==0:
            r_boxes_rot = np.stack([r_boxes[:n_candidates,1],r_boxes[:n_candidates,0],r_boxes[:n_candidates,2]], axis = -1)
            mask = [ sum((i >= r_boxes_rot).sum(1)==3)>=1 for i in bbox_sc]
        in_state = np.array([ np.stack([np.zeros_like(b),np.zeros_like(b),b/mxh,(b!=mxh).astype('float')], axis=-1) for b in bbox_type[mask]])
        loading_loc_c = np.zeros((sum(mask),)+loading_loc_shape) # 적입 위치
        in_loading = np.zeros((sum(mask), K, max_size, n_channel//2)) # 적입 규격
        in_remain = np.array([m_mat[:num_max_remain]]*num_bbox_type).copy()  
        in_remain = in_remain[mask] 
        in_cbm = init_cbm(cbm_bbox[mask],bbox_cbm_mx, cbm_mbox[ith_data], boxes_idx, num_max_remain, K) 
        in_w = init_weight(sum(mask), w_mbox, boxes_idx, num_max_remain, K)
        # 대박스 규격 선택
        action_idx = agent.get_action(in_state, loading_loc_c, in_remain, in_loading, in_cbm, in_w)
        bbox_idx = np.where(mask)[0][action_idx]
        env.reset(bbox_idx)
        history.append(in_state[action_idx])
        h_load.append(loading_loc_c[action_idx])
        h_remain_size.append(in_remain[action_idx])
        h_load_size.append(in_loading[action_idx])
        h_cbm.append(in_cbm[action_idx])
        h_weight.append(in_w[action_idx])
        s_bbox_cbm = df_bbox.iloc[env.bbox_idx]['CBM']
        bbox_l, bbox_b = bbox_sc[bbox_idx][0], bbox_sc[bbox_idx][1]
        state_wsum = np.zeros((bbox_l, bbox_b)) #무게 균형을 계산하기 위한 행렬 초기화
        is_last.append(False)
        reward_w.append(0)
        
        while not done:#중박스에 대해 반복##############
            state = env.container_s.copy()
            state_h = env.container_h.copy()
            state_w = env.container_w.copy()
            global_step += 1
            step += 1
            # CBM
            cbm_all_ratio = cbm_all/s_bbox_cbm
            # 적재 위치 계산 ########################
            k = 1 #min(K, len(r_boxes))
            selected, selected_idx = cbn_select_boxes(r_boxes[:n_candidates],boxes_idx[:n_candidates], k) # 조합
            s_order, s_order_idx = get_selected_order(selected, selected_idx, k) #순열
            s_order, s_order_idx = rot_one_order(s_order, s_order_idx) # 회전
            #s_order, s_order_idx = merge_order_rep(s_order, s_order_idx, selected, r_boxes ,boxes_idx, max_k) 
            add_skip = False #if len_group == 0 else True #add_skip=False: 적입하지 않는 action은 없음
            order_idx_c, num_loading_c, loading_idx_c, loading_size_c, loading_xyz_c, loading_loc_c, next_state_c, next_h_c, next_w_c \
                = get_selected_location(s_order, s_order_idx, state, state_h, state_w, env.height, K, cbm_reward ,cbm_all_ratio, 
                                        w_mbox, add_skip )
            # action ########################
            if np.sum(num_loading_c) != 0: # 적입하는 경우가 한 가지 이상 있는 경우
                idx_c = [s_order_idx[i] for i in order_idx_c]
                in_state, in_remain, in_loading = raw2input(state, state_h, state_w, env.bbox, m_mat, mbox_mat[ith_data],
                                                            s_bbox_cbm, idx_c, K, mxh)
                in_cbm = get_in_cbm(s_bbox_cbm, bbox_cbm_mx, cbm_mbox[ith_data], boxes_idx, loaded_idx, len_group,idx_c, num_max_remain, K)
                in_w = get_in_weight(w_mbox, boxes_idx, idx_c, num_max_remain, K, state_wsum, loading_loc_c)
                if np.sum(num_loading_c) == 1: action_idx = 0 #가능한 action 수가 1개인 경우
                else: action_idx = agent.get_action(in_state, np.array(loading_loc_c), in_remain, in_loading, in_cbm, in_w) # 두 가지 이상인 겨우
            else: #하나도 적입하지 못한 경우(취할 action이 없는 경우)
                action_idx = 0 
                in_state, in_remain, in_loading = \
                    raw2input(state, state_h, state_w, env.bbox, m_mat, mbox_mat[ith_data], s_bbox_cbm, [], K, mxh)
                loading_loc_c = np.zeros((1,)+loading_loc_shape)#np.zeros((1, mxl, mxb, K)) 
                next_state_c =  state[np.newaxis].copy()
                next_h_c = state_h[np.newaxis].copy()
                next_w_c = state_w[np.newaxis].copy()
                in_cbm = get_in_cbm(s_bbox_cbm, bbox_cbm_mx, cbm_mbox[ith_data], boxes_idx, loaded_idx, len_group, [], num_max_remain, K)
                in_w = get_in_weight(w_mbox, boxes_idx, [], num_max_remain, K, state_wsum, [])
                
                
            # 다음 step ################################
            if np.sum(num_loading_c) == 0 or (np.sum(num_loading_c)!=0 and num_loading_c[action_idx]==0): 
                # 주어진 중박스 중 하나도 적재하지 못한 경우, 적재하지 않는 action을 선택할 경우
                r_boxes = get_remain(r_boxes[:n_candidates], r_boxes) # 해당 범위의 박스들 제외
                m_mat = drop_remain(m_mat, boxes_idx[:n_candidates])
                boxes_idx = boxes_idx[n_candidates:]
                done = True
            else: # 한 가지 이상의 action 옵션이 있는 경우(적재 가능한 경우)
                env.step(next_state_c[action_idx], next_h_c[action_idx], next_w_c[action_idx])  # env의 다음 state
                # 업데이트
                order_idx = order_idx_c[action_idx]
                loading_idx = loading_idx_c[action_idx]
                len_group += num_loading_c[action_idx] # bbox
                # index 업데이트
                loaded_idx += loading_idx # 적입된 박스 인덱스
                boxes_idx = np.setdiff1d(boxes_idx, s_order_idx[order_idx]) # 남은 박스의 인덱스
                # boxes_idx = np.setdiff1d(boxes_idx, loading_idx) 
                # 남은 박스 업데이트
                r_boxes = boxes_all_sc[boxes_idx]
                m_mat = mbox_mat[ith_data].copy()
                m_mat = add_loading(m_mat, loaded_idx, len_group)
                m_mat = drop_remain(m_mat, loaded_idx)
                # cbm
                cbm_reward += (np.sum(cbm_all_ratio[loading_idx]))#/df_bbox.iloc[env.bbox_idx]['CBM'])
                # 사용된 박스, 위치 업데이트
                used_boxes = used_boxes + loading_size_c[action_idx] #사용된 박스 업데이트
                pred_pos = pred_pos + loading_xyz_c[action_idx] #예측된 위치 업데이트
                # 무게합 상태 업데이트
                state_wsum = state_wsum + loading_loc_c[action_idx][:bbox_l, :bbox_b, 1] # 업데이트
                
            #남은 박스가 없음 or 높이맵이 모두 채워짐 or cbm 모두 채워짐 or 적입할 수 없음
            if len(r_boxes) == 0 or np.sum(env.container_h != env.height) == 0 or cbm_reward>=1:
                done = True
            if done:
                env_rewards.append(cbm_reward)   
            ################################################################################ 두 번째 while 끝
        ################################################################################ 첫 번째 while 시작
        #print('m_mat 2',np.sum(m_mat[:,:,0]),np.sum(m_mat[:,:,1]),np.sum(m_mat[:,:,2]),np.sum(m_mat[:,:,3]))
        boxes_idx = np.setdiff1d(np.arange(len(boxes_all_sc)), loaded_idx)
        r_boxes = boxes_all_sc[boxes_idx]
        if len_group>0: used_bbox.append([env.bbox_idx]*len_group)
        m_mat = drop_remain(mbox_mat[ith_data], loaded_idx) #적입된 상자는 0으로 초기화
        #print('m_mat 3',np.sum(m_mat[:,:,0]),np.sum(m_mat[:,:,1]),np.sum(m_mat[:,:,2]),np.sum(m_mat[:,:,3]))
    ################################################################################ 

    log = "=====episode:{:5d}| ".format(e)
    log += "reward:{:2d}, {:.3f} (".format(len(env_rewards), np.mean(env_rewards))
    log += ', '.join('{:.3f}'.format(k) for k in env_rewards)
    log += ")/time:{:.2f}".format(time.time()-st)
    print(log)
    agent.avg_q_max, agent.avg_loss = 0, 0
    
    
    if is_pred:
        i = 0
        for p in used_bbox:
            p_loaded_idx = loaded_idx[i:i+len(p)]
            positions =  np.array(pred_pos)[i:i+len(p)]
            positions[:, :2] = positions[:, :2] /sc
            sizes =  np.array(used_boxes)[i:i+len(p)]
            sizes[:, :2] = sizes[:, :2] /sc
            # 대박스 규격
            bbox_ = bbox_sc[p[0]].copy()
            # 높이 조정
            positions[:,2] = positions[:,2] - (mxh-bbox_[2])
            # append
            p_bbox = df_bbox.iloc[p[0]]
            p_x = df_p.iloc[p_loaded_idx].copy()
            p_x['pack_no'] = 'resid_'+str(pack_no)
            p_x['packing_rate_cbm'] = (p_x['cbmsum_per_mbox']).sum() / p_bbox['CBM']
            p_x['packing_rate_volume'] = (p_x['M_L']*p_x['M_B']*p_x['M_H']).sum() / (p_bbox['L']*p_bbox['B']*p_bbox['H'])
            p_x['x'] = positions[:, 0]
            p_x['y'] = positions[:, 1]
            p_x['z'] = positions[:, 2]
            p_x['M_L2'] = sizes[:, 0]
            p_x['M_B2'] = sizes[:, 1]
            #p_x[['P_bbox_cd','P_L','P_B','P_H','P_CBM']] = p_bbox.values
            p_x[['P_bbox_cd','P_H','P_CBM']] = p_bbox[['CASE_CD', 'H', 'CBM']].values
            p_x[['P_L','P_B']] = bbox_[:2] /sc
            pk = pk.append(p_x)
            pack_no += 1
            i += len(p)    
    #if e==1: break
print('total training time', time.time() - tot_st)
pk.to_csv('data/pack/' + mi+ '_'+ mbox_type +'_hete.csv',index=False)

x = pk.groupby(['pack_no'])['packing_rate_cbm'].agg('first')
#plt.hist(x)
print(mi+'_'+mbox_type+'mean: {:.4f}, medi: {:.4f}, mean>.5: {:.4f}, medi>.5: {:.4f} '.format(np.mean(x),np.median(x),
                                                                                               np.mean(x[x>0.5]), np.median(x[x>0.5])))