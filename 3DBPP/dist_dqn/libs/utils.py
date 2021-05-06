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

def random_action_idx(f_upleft):
    if len(f_upleft) == 0: return -1
    else: return np.random.choice(range(len(f_upleft)),1)[0]

def cbn_select_boxes(boxes, k=5):
    s_boxes = np.array(list(itertools.combinations(boxes , k)))
    s_boxes = np.unique(s_boxes, axis=0)
    return s_boxes

def idx_to_order(idx, K):
    order_list = list(itertools.permutations(range(K)))
    order = order_list[idx]
    order = list(order)
    return order

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

def raw2input(state_h, n_candidates, r_boxes,  num_max_remain, num_selected, loading_size_c, e_h=20):
    e_l, e_b = state_h.shape
    state_h_c = np.array([state_h]*n_candidates).reshape((-1, e_l,e_b,1))
    r_boxes_c = np.array([padding_boxes(get_remain(l, r_boxes), num_max_remain) for l in loading_size_c]).astype('int')
    loading_c = np.array([padding_boxes(l, num_selected) for l in loading_size_c]).astype('int')
    r_mat_c = np.array(([ [size2matrix(j, e_l, e_b) for j in i] for i in r_boxes_c  ]))
    loading_mat_c =  np.array(([ [size2matrix(j, e_l, e_b) for j in i] for i in loading_c  ]))

    state_h_c = (np.array(state_h_c)/e_h).astype(np.float32)
    r_mat_c = (np.array(r_mat_c)/e_h).astype(np.float32)
    loading_mat_c = (np.array(loading_mat_c)/e_h).astype(np.float32)
    
    r_mat_c = r_mat_c.transpose((0,2,3,1))
    loading_mat_c = loading_mat_c.transpose((0,2,3,1))
    return state_h_c, r_mat_c, loading_mat_c

def get_loaded_h(state):
    env_l, env_b, env_h = state.shape
    idx = np.where(state == 1)
    h = pd.DataFrame(np.transpose(idx, (1,0)))
    h.columns = ['0','1','2']
    h = h.groupby(['0','1']).agg({'0':'first','1':'first','2':'max'}).values
    state_h = np.zeros((env_l, env_b))
    state_h[h[:,0],h[:,1]] = h[:,2]+1
    return state_h

def get_fixed_xyz(box, state):
    env_l, env_b, env_h = state.shape
    state_h = get_loaded_h(state)
    next_state = state.copy()
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
        f_upleft = f_upleft[area == np.min(area)] #가장 낮게 적입할 수 있는 위치
        z =  state_h[f_upleft[:,0], f_upleft[:, 1]] # z 좌표
        loc_xyz = np.concatenate([f_upleft, z[:, np.newaxis]], axis = -1) #xyz 좌표
        fixed_xyz = loc_xyz[np.lexsort((loc_xyz[:,1],loc_xyz[:,0],loc_xyz[:,2]))] #하나 선택
        loc_xyz = loc_xyz[0].astype('int')
        
        next_state = get_next_state(state, loc_xyz[:2], bxl,bxb,bxh)
        
    return loc_xyz, next_state  


def get_next_state(state, upleft,bxl,bxb,bxh):
    state_h = get_loaded_h(state)
    loading_area_h =state_h[upleft[0]:upleft[0]+bxl, upleft[1]:upleft[1]+bxb]
    max_h = np.max(loading_area_h).astype('int')
    
    next_state = state.copy()
    next_state[upleft[0]:upleft[0]+bxl, upleft[1]:upleft[1]+bxb, max_h:bxh + max_h] = 1

    return next_state 

def get_selected_order(selected, k):
    selected_order = []
    perm_idx = list(itertools.permutations(range(k)))
    for s in selected:
        for i in range(len(perm_idx)):
            p = perm_idx[i] # 순서 선택
            selected_order.append( s[list(p)] )
    selected_order = np.stack(selected_order)
    selected_order = np.unique(selected_order, axis=0)
    return selected_order 

def get_loaded_mh(s_loc, env_l, env_b, env_h):
    loaded_m = np.mean(s_loc, axis = -1)
    idx = np.where(s_loc == 1)
    h = pd.DataFrame(np.transpose(idx, (1,0)))
    h.columns = ['0','1','2']
    h = h.groupby(['0','1']).agg({'0':'first','1':'first','2':'max'}).values
    loaded_h = np.zeros(( env_l, env_b ))
    loaded_h[h[:,0],h[:,1]] = h[:,2]+1
    loaded_h = loaded_h/env_h # scaling
    
    loaded_mh = np.stack([loaded_m, loaded_h], axis = -1)
    loaded_mh = loaded_mh.astype(np.float32)
    return loaded_mh

def get_selected_location(s_order, state_org):
    e_l, e_b, e_h = state_org.shape
    # 정해진 순서에 따라 하나씩 적재
    s_locs, loading_pos_c, loading_size_c, next_state_c, num_loaded_c  = [],[],[],[],[]
    next_state, next_h_c = [], []
    
    for boxes in s_order:
        #초기화
        state = state_org.copy()
        state_h = get_loaded_h(state)
        next_state = state.copy()
        next_h = state_h.copy()
        loading_size, loading_pos = [],[]
        num_loaded = 0
        s_loc = np.zeros((e_l,e_b,e_h))
        for box in boxes:
            if np.sum(box)==0:
                fixed_xyz = []
            else:
                fixed_xyz, next_state = get_fixed_xyz(box, state) #박스의 좌표와 next_state
            if len(fixed_xyz) == 0:
                continue
            state = next_state.copy() # state 업데이트 
            next_h = get_loaded_h(next_state) #next_h 업데이트            
            num_loaded += 1 # 카운트            
            loading_size.append(box)
            loading_pos.append(fixed_xyz)
            # location
            x,y,z = fixed_xyz.astype('int')
            l,b,h = box
            s_loc[x:x+l, y:y+b, z:z+h] = 1
        
        if len(loading_size)==0:
            loading_size.append(np.zeros_like(box))
            loading_pos.append(np.zeros_like(box))
        
        s_locs.append(s_loc)
        num_loaded_c.append(num_loaded)
        loading_size_c.append(loading_size)
        loading_pos_c.append(loading_pos)
        next_state_c.append(next_state)
        next_h_c.append(next_h)
        
    s_locs = np.stack(s_locs) #(N, L, B, H)
    return s_locs, num_loaded_c, loading_size_c, loading_pos_c, next_state_c, next_h_c

def get_unique(s_order, s_loc_c, num_loaded_box_c, loading_size_c, loading_pos_c, next_cube_c , next_state_c, loaded_mh_c, in_state, in_r_boxes, in_loading):
    loaded_mh_c_u, idx1 = np.unique(loaded_mh_c, return_index=True, axis=0)
    in_r_boxes_u, idx2 = np.unique(in_r_boxes, return_index=True, axis=0)
    idx = np.union1d(idx1, idx2)
    if len(loaded_mh_c) != len(idx):
        #print('reduced',len(loaded_mh_c), len(idx), idx)
        #print(loading_size_c)
        #for i in range(len(loaded_mh_c)):
        #    plt.imshow(loaded_mh_c[i,:,:,0])
        #    plt.show()
        #    plt.imshow(loaded_mh_c[i,:,:,1])
        #    plt.show()
        loaded_mh_c = loaded_mh_c[idx]
        in_r_boxes = in_r_boxes[idx]
        s_order = s_order[idx]
        s_loc_c= s_loc_c[idx]
        num_loaded_box_c= [num_loaded_box_c[i] for i in idx]
        loading_size_c = [loading_size_c[i] for i in idx]
        loading_pos_c = [loading_pos_c[i] for i in idx]
        next_cube_c = [next_cube_c[i] for i in idx]
        next_state_c = [next_state_c[i] for i in idx]
        in_state = in_state[idx]
        in_loading = in_loading[idx]
    return s_order, s_loc_c, num_loaded_box_c, loading_size_c, loading_pos_c, next_cube_c , next_state_c, loaded_mh_c, in_state, in_r_boxes, in_loading


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
    def __init__(self,length = 20, breadth = 20, height = 20, bbox = np.zeros((20, 20, 20))):
        super(Bpp3DEnv, self).__init__()
        self.length=length
        self.breadth=breadth
        self.height=height
        self.bbox = bbox
        self.container_h = np.zeros((self.length,self.breadth))
        self.container = self.bbox.copy()
        self.update_h()
    
    def update_h(self):
        idx = np.where(self.container == 1)
        h = pd.DataFrame(np.transpose(idx, (1,0)))
        h.columns = ['0','1','2']
        h = h.groupby(['0','1']).agg({'0':'first','1':'first','2':'max'}).values
        self.zero_h()
        self.container_h[h[:,0],h[:,1]] = h[:,2]+1
        return self.container_h
    
    def convert_state(self, new_container):
        self.container = new_container
        self.update_h()
    
    def next_state(self, upleft,bxl,bxb,bxh):
        next_container_h = self.container_h.copy()
        loading_area_h = self.container_h[upleft[0]:upleft[0]+bxl, upleft[1]:upleft[1]+bxb]
        max_h = np.max(loading_area_h).astype('int')
        next_container_h[upleft[0]:upleft[0]+bxl,upleft[1]:upleft[1]+bxb] = bxh + max_h
        
        next_container = self.container.copy()
        next_container[upleft[0]:upleft[0]+bxl, upleft[1]:upleft[1]+bxb, max_h:bxh + max_h] = 1
        
        return next_container, next_container_h
    
    def step(self, upleft,bxl,bxb,bxh):
        n_s, n_h = self.next_state(upleft,bxl,bxb,bxh)
        self.convert_state(n_s)
        return n_s
    
    def reset(self):
        #self.container = np.zeros((self.length,self.breadth, self.height))
        #self.container_h = np.zeros((self.length,self.breadth))
        self.container = self.bbox.copy()#np.zeros((self.length, self.breadth, self.height))
        self.update_h()
        
    def zero_h(self):
        self.container_h = np.zeros((self.length,self.breadth))
        
    def terminal_reward(self):
        fill = np.sum(self.container) - np.sum(self.bbox)
        valid = self.length*self.breadth*self.height - np.sum(self.bbox)
        #return np.sum(self.container)/(self.length*self.breadth*self.height)
        return fill/valid


##################################################################################


