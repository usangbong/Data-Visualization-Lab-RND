import numpy as np
import itertools
from random import shuffle
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import pandas as pd

def padding_boxes(box, max_boxes):
    box = np.array(box)
    padded = np.concatenate([box,np.zeros((max_boxes-len(box),3))])
    return padded

# def random_action_idx(f_upleft):
#     if len(f_upleft) == 0: return -1
#     else: return np.random.choice(range(len(f_upleft)),1)[0]

# def idx_to_order(idx, K):
#     order_list = list(itertools.permutations(range(K)))
#     order = order_list[idx]
#     order = list(order)
#     return order

def cbn_select_boxes(boxes, box_idx, k):
    s_boxes = np.array(list(itertools.combinations(boxes , k)))
    s_boxes, unique_idx = np.unique(s_boxes, axis=0, return_index=True)
    comb_idx =  np.array(list(itertools.combinations( range(len(boxes)) , k))) #C,k
    comb_idx = np.array(comb_idx)[unique_idx] #C,k
    comb_idx = np.array( [box_idx[i] for i in comb_idx] )
    return s_boxes, comb_idx

def get_selected_order(selected, comb_idx, k):
    selected_order = []
    order_idx = []
    perm_idx = list(itertools.permutations(range(k)))
    for s,c in zip(selected, comb_idx):
        for i in range(len(perm_idx)):
            p = perm_idx[i] # 순서 선택
            selected_order.append( s[list(p)] )
            order_idx.append(c[list(p)])
    selected_order = np.stack(selected_order)
    selected_order, unique_idx = np.unique(selected_order, axis=0, return_index=True)
    order_idx = np.stack(order_idx)
    order_idx = order_idx[unique_idx]
    return selected_order, order_idx 

def get_remain(s_boxes, r_boxes):
    for i in s_boxes:
        if i in r_boxes:
            drop_idx = np.where(np.all(i==r_boxes,axis=1))[0][0]
            r_boxes = np.delete(r_boxes, (drop_idx), axis=0)
    return r_boxes

def size2matrix(box, e_l, e_b):
    # box (3,)
    l, b = box[:2]
    box = np.ones((l,b)) * box[2]
    padded = np.pad(box, ((0, e_l-l), (0, e_b - b)), mode='constant', constant_values=0)
    return padded

def raw2input(state_s, state_h, r_boxes,  num_max_remain, num_selected, loading_size_c, e_h=20):
    n_combs = len(loading_size_c)
    e_l, e_b = state_h.shape
    state = np.stack([state_s, state_h],axis = -1)
    state_c = np.array([state]*n_combs).reshape((-1, e_l,e_b,2))
    r_boxes_c = np.array([padding_boxes(get_remain(l, r_boxes), num_max_remain) for l in loading_size_c]).astype('int')
    loading_c = np.array([padding_boxes(l, num_selected) for l in loading_size_c]).astype('int')
    r_mat_c = np.array(([ [size2matrix(j, e_l, e_b) for j in i] for i in r_boxes_c  ]))
    loading_mat_c =  np.array(([ [size2matrix(j, e_l, e_b) for j in i] for i in loading_c  ]))
    # scaling
    state_c = (np.array(state_c)/e_h).astype(np.float32)
    r_mat_c = (np.array(r_mat_c)/e_h).astype(np.float32)
    loading_mat_c = (np.array(loading_mat_c)/e_h).astype(np.float32)
    # transpose
    r_mat_c = r_mat_c.transpose((0,2,3,1))
    loading_mat_c = loading_mat_c.transpose((0,2,3,1))
    return state_c, r_mat_c, loading_mat_c

def get_fixed_loc(box, state_h, env_h):
    env_l, env_b = state_h.shape
    bxl, bxb, bxh = box[0], box[1], box[2]
    f_loc = np.where(state_h + bxh <= env_h) # 환경의 높이보다 state 작은 위치
    f_upleft = np.stack([f_loc[0], f_loc[1]], axis=-1) # array 형태로 변환
    f_upleft = f_upleft[f_upleft[:,0] + bxl  <= env_l ] # row 넘어가면 삭제
    f_upleft = f_upleft[f_upleft[:,1] + bxb <= env_b ] # columns 넘어가면 삭제
    area = np.array([state_h[i:i+bxl, j:j+bxb] for i,j in f_upleft])
    loc_xyz = []
    if len(f_upleft) > 0 and len(area)>0:
        #print(area.shape, f_upleft.shape, state_h.shape)
        area = np.max(area, axis=(1,2)) # 적입할 수 있는 위치의 높이
        f_upleft = f_upleft[area+ bxh <= env_h] # 높이 넘으면 삭제
        area = area[area+ bxh <= env_h]
    if len(f_upleft) > 0 and len(area)>0:
        #f_upleft = f_upleft[area == np.min(area)] #가장 낮게 적입할 수 있는 위치
        #z =  state_h[f_upleft[:,0], f_upleft[:, 1]] # z 좌표
        loc_xyz = np.concatenate([f_upleft, area[:, np.newaxis]], axis = -1) #xyz 좌표
        loc_xyz = loc_xyz[np.lexsort((loc_xyz[:,1],loc_xyz[:,0],loc_xyz[:,2]))] #하나 선택
        loc_xyz = loc_xyz[0].astype('int')
        
    return loc_xyz

def get_next_state(state, state_h, upleft,bxl,bxb,bxh):
    next_state = state.copy()
    next_state_h = state_h.copy()
    next_state[upleft[0]:upleft[0]+bxl, upleft[1]:upleft[1]+bxb] += bxh
    loading_area_h =state_h[upleft[0]:upleft[0]+bxl, upleft[1]:upleft[1]+bxb]
    max_h = np.max(loading_area_h).astype('int')
    next_state_h[upleft[0]:upleft[0]+bxl, upleft[1]:upleft[1]+bxb] = max_h+bxh
    return next_state, next_state_h 


def get_selected_location(s_order, s_order_idx, state_org, state_h_org, e_h, k):
    # 초기화
    e_l, e_b = state_org.shape
    order_idx_c = []
    loading_size_c, loading_idx_c, loading_xyz_c, num_loading_c, loading_loc_c  = [],[],[],[],[]
    next_state_c, next_state_h_c = [], []
    # 정해진 순서에 따라 하나씩 적재
    for order_idx, (boxes, element_idx) in enumerate(zip(s_order, s_order_idx)):
        # 초기화
        state = state_org.copy()
        state_h = state_h_org.copy()
        next_state = state.copy()
        next_state_h = state_h.copy()
        loading_size, loading_idx, loading_xyz = [],[],[]
        loading_loc = np.zeros((e_l,e_b,k))
        num_loading = 0
        # 적재 시작
        for i, (box,idx) in enumerate(zip(boxes, element_idx)): #boxes의 길이는 k
            fixed_xyz = get_fixed_loc(box, state_h, e_h) #박스의 좌표와 next_state
            ### 해당 중박스를 적재하지 못한 경우에 스킵
            if len(fixed_xyz) == 0: 
                continue
            ### 해당 중박스를 적재 했을 경우 
            # 적재 위치
            loading_loc[fixed_xyz[0]:fixed_xyz[0]+box[0], fixed_xyz[1]:fixed_xyz[1]+box[1], i] = fixed_xyz[2]+ box[2]
            # 다음 상태 계산
            next_state, next_state_h = get_next_state(state, state_h, fixed_xyz[:2], box[0], box[1], box[2])            
            # state 업데이트
            state = next_state.copy() 
            state_h = next_state_h.copy()            
            # append
            num_loading += 1 # 카운트
            loading_idx.append(idx)
            loading_size.append(box)
            loading_xyz.append(fixed_xyz)            
        
        ########################################
        #if num_loading != 0: #하나 이상의 중박스를 적재했을 경우 -> append
        # append (중박스를 하나도 적재하지 않은 경우 포함, 중복 데이터만 제외)
        
        # scaling
        loading_loc = loading_loc/e_h 
        # 중복 제외: loading_loc, loading_size가 동일하면 append 제외
        if len(loading_loc_c) > 0:
            idx1 = [i for i, x in enumerate(loading_loc_c) if (x==loading_loc).all()]
            idx2 = [i for i, x in enumerate(loading_size_c) if np.array((np.array(x)==loading_size)).all()]
            num_inter = list(set(idx1) & set(idx2))
            if len(num_inter) > 0:
                #print('duplicate',set(idx1) & set(idx2), loading_size_c, loading_size, fixed_xyz)
                continue
        # append
        order_idx_c.append(order_idx)
        num_loading_c.append(num_loading)
        loading_idx_c.append(loading_idx)
        loading_size_c.append(loading_size)
        loading_xyz_c.append(loading_xyz)
        loading_loc_c.append(loading_loc)
        next_state_c.append(next_state)
        next_state_h_c.append(next_state_h)
        
    return order_idx_c, num_loading_c, loading_idx_c, loading_size_c, loading_xyz_c, loading_loc_c, next_state_c, next_state_h_c



################################################################visualization 
def cuboid_data2(o, size=(1,1,1)):
    X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
         [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
         [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
         [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:,:,i] *= size[i]
    X += np.array(o)
    return X

def plotCubeAt2(positions,sizes=None,colors=None,a=0.5, **kwargs):
    if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    g = []
    for p,s,c in zip(positions,sizes,colors):
        g.append( cuboid_data2(p, size=s) )
    return Poly3DCollection(np.concatenate(g),facecolors=np.repeat(colors,6), alpha=a, **kwargs)

def get_colors(n_box):
    color_names=["crimson","limegreen","grey","brown","orange","olive","blue","purple","yellow","pink","skyblue","red","aqua","gold"]
    colors = color_names*(n_box//len(color_names))+color_names[:n_box%len(color_names)]
    return colors

def vis_box(sizes,positions,fs=(3,3),mn=-5, mx=25):
    colors = get_colors(len(positions))
    fig = plt.figure(figsize=fs)
    ax = fig.gca(projection='3d')
    ax.set_aspect('auto')
    pc = plotCubeAt2(positions,sizes,colors=colors, edgecolor="w")
    ax.add_collection3d(pc)    
    ax.set_xlim([mn,mx])
    #ax.set_ylim([-5,25])
    ax.set_ylim([mx,mn])
    ax.set_zlim([mn,mx])
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.show()
    
def make_ax(grid=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.grid(grid)
    return ax
def plot_voxel(t):
    ax = make_ax(True)
    ax.voxels(t,  edgecolors='gray', shade=False, alpha = 0.8)
    plt.show()
    
################################################################ Environment  
class Bpp3DEnv():#(gym.Env):
    #metadata = {'render.modes': ['human']}
    #
    def __init__(self,length = 20, breadth = 20, height = 20, bbox = np.zeros((20, 20))):
        super(Bpp3DEnv, self).__init__()
        self.length=length
        self.breadth=breadth
        self.height=height
        self.bbox = bbox
        self.container_h = self.bbox.copy() #(L,B)
        self.container_s = self.bbox.copy() #(L,B)
        
    def step(self, next_container_s, next_container_h):
        self.container_s = next_container_s
        self.container_h = next_container_h
    
    def reset(self):
        self.container_s = self.bbox.copy()
        self.container_h = self.bbox.copy()
        
    def terminal_reward(self):
        fill = np.sum(self.container_s) - np.sum(self.bbox)
        valid = self.length*self.breadth*self.height - np.sum(self.bbox)
        #return np.sum(self.container)/(self.length*self.breadth*self.height)
        return fill/valid


##################################################################################


