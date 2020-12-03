import numpy as np
import matplotlib.pyplot as plt
from random import shuffle

def generation_input_v0(N_epi=1):
    np.random.seed(seed=100)
    X_input=[]
    for i in range(N_epi):
        #middle box info
        N_mdd=np.random.choice(list(range(200,300)), 1)
        mdd_b=np.random.choice(list(range(10,21)), N_mdd)
        mdd_l=np.random.choice(list(range(10,21)), N_mdd)
        mdd_h=np.random.choice(list(range(10,21)), N_mdd)
        mdd_w=np.random.uniform(low=5.0, high=18.0, size=N_mdd)
        X_input.append([list(a) for a in zip(mdd_b,mdd_l,mdd_h,mdd_w)])
    return X_input

def generation_2dbox(N_epi=1,c_l=20,c_b=20):
    #c_l, c_h: length, height
    np.random.seed(seed=100)
    epi_input=[]
    epi_gt_upleft=[]
    
    for i in range(N_epi):
        N_mdd=np.random.choice(list(range(25,30)), 1)
        
        X_input=[[c_l,c_b]]
        gt_upleft=[[0,0]]
        #X_input=[[int(c_l/2),int(c_b/2)]]*4 #4분할
        #gt_upleft=[[0,0],[int(c_l/2),0],[0,int(c_b/2)],[int(c_l/2),int(c_b/2)]]
        #N_mdd-=4
        
        while(len(X_input)<N_mdd):
            idx=np.random.choice(list(range(len(X_input))), 1)[0]#pop an item randomly from X_input
            pop_item=X_input.pop(idx)#[l, b]
            pop_gt_upleft=gt_upleft.pop(idx)
            idx=np.random.choice([0,1],1)[0]#choose an axis randomly
            
            if pop_item[idx]<=3:#if pop_item[idx]==1:
                X_input.append(pop_item)
                gt_upleft.append(pop_gt_upleft)
            else:#item split
                #pos=np.random.choice(list(range(1,pop_item[idx]-1)),1)[0]
                pos=np.random.choice(list(range(1+1,pop_item[idx]-1)),1)[0]#choose a position randomly - distance
                #item L,B
                item1=pop_item.copy()
                item2=pop_item.copy()
                item1[idx]=pos
                item2[idx]=pop_item[idx]-pos
                X_input+=[item1,item2]
                #gt upleft
                itme2_upleft=pop_gt_upleft.copy()
                itme2_upleft[idx] += pos
                gt_upleft+=[pop_gt_upleft,itme2_upleft]
        
        # 랜덤 순서
        #z = list(zip(X_input, gt_upleft))
        #shuffle(z)
        #X_input, gt_upleft = zip(*z)
        
        #크기순 정렬
        #s=[i*j for i,j in X_input]
        #s_idx=sorted(range(len(s)), key=lambda k: s[k])
        #X_input=np.array(X_input)[list(reversed(s_idx))]
        #gt_upleft=np.array(gt_upleft)[list(reversed(s_idx))]
        
        epi_input.append(X_input)
        epi_gt_upleft.append(gt_upleft)
    return epi_input,epi_gt_upleft#np.array(X_input)#_input

def generation_3dbox_v0(N_epi=1,c_l=20,c_b=20,c_h=20):
    #c_l, c_b, c_h: length, breadth, height
    #np.random.seed(seed=100)
    epi_input=[]
    epi_gt_upleft=[]
    
    for i in range(N_epi):
        N_mdd=22#np.random.choice(list(range(15,20)), 1)
        
        X_input=[[c_l,c_b,c_h]]
        gt_upleft=[[0,0,0]]
        #X_input=[[int(c_l/2),int(c_b/2),int(c_h/2)]]*8 #8분할
        #gt_upleft=[[0,0,0],[int(c_l/2),0,0],[0,int(c_b/2),0],[int(c_l/2),int(c_b/2),0],
        #          [0,0,int(c_h/2)],[int(c_l/2),0,int(c_h/2)],[0,int(c_b/2),int(c_h/2)],[int(c_l/2),int(c_b/2),int(c_h/2)]]
        #N_mdd-=8
        
        while(len(X_input)<N_mdd):
            idx=np.random.choice(list(range(len(X_input))), 1)[0]#pop an item randomly from X_input
            pop_item=X_input.pop(idx)#[l, b]
            pop_gt_upleft=gt_upleft.pop(idx)
            idx=np.random.choice([0,1,2],1)[0]#choose an axis randomly
            if pop_item[idx]<=3:#if pop_item[idx]==1:
                X_input.append(pop_item)
                gt_upleft.append(pop_gt_upleft)
            else:#item split
                pos=np.random.choice(list(range(1,pop_item[idx])),1)[0]#choose a position randomly - distance
                #item L,B
                item1=pop_item.copy()
                item2=pop_item.copy()
                item1[idx]=pos
                item2[idx]=pop_item[idx]-pos
                X_input+=[item1,item2]
                #gt upleft
                itme2_upleft=pop_gt_upleft.copy()
                itme2_upleft[idx] += pos
                gt_upleft+=[pop_gt_upleft,itme2_upleft]
         
        #무게 포함
        #mdd_w=np.random.uniform(low=5.0, high=18.0, size=N_mdd)
        #X_input=[list(a[0] + [a[1]]) for a in zip(X_input,mdd_w)]
        
        #순서 -> 랜덤 정렬
        #z = list(zip(X_input, gt_upleft))
        #shuffle(z)
        #X_input, gt_upleft = zip(*z)
        
        #순서 -> 크기순 정렬
        #s=[i*j*q for i,j,q in X_input]
        #s_idx=sorted(range(len(s)), key=lambda k: s[k])
        #X_input=np.array(X_input)[list(reversed(s_idx))]
        #gt_upleft=np.array(gt_upleft)[list(reversed(s_idx))]
        
        epi_input.append(X_input)
        epi_gt_upleft.append(gt_upleft)
    return epi_input,epi_gt_upleft#np.array(X_input)#_input


def generation_3dbox(N_epi=1,c_l=20,c_b=20,c_h=20):
    #c_l, c_b, c_h: length, breadth, height
    #np.random.seed(seed=100)
    epi_input=[]
    epi_gt_upleft=[]
    
    for i in range(N_epi):
        N_mdd=22#np.random.choice(list(range(15,20)), 1)
        
        X_input=[[c_l,c_b,c_h]]
        gt_upleft=[[0,0,0]]
        #X_input=[[int(c_l/2),int(c_b/2),int(c_h/2)]]*8 #8분할
        #gt_upleft=[[0,0,0],[int(c_l/2),0,0],[0,int(c_b/2),0],[int(c_l/2),int(c_b/2),0],
        #          [0,0,int(c_h/2)],[int(c_l/2),0,int(c_h/2)],[0,int(c_b/2),int(c_h/2)],[int(c_l/2),int(c_b/2),int(c_h/2)]]
        #N_mdd-=8
        
        while(len(X_input)<N_mdd):
            idx=np.random.choice(list(range(len(X_input))), 1)[0]#pop an item randomly from X_input
            pop_item=X_input.pop(idx)#[l, b]
            pop_gt_upleft=gt_upleft.pop(idx)
            idx=np.random.choice([0,1,2],1)[0]#choose an axis randomly
            if pop_item[idx]<=3:#if pop_item[idx]==1:
                X_input.append(pop_item)
                gt_upleft.append(pop_gt_upleft)
            else:#item split
                pos=np.random.choice(list(range(1,pop_item[idx])),1)[0]#choose a position randomly - distance
                #item L,B
                item1=pop_item.copy()
                item2=pop_item.copy()
                item1[idx]=pos
                item2[idx]=pop_item[idx]-pos
                X_input+=[item1,item2]
                #gt upleft
                itme2_upleft=pop_gt_upleft.copy()
                itme2_upleft[idx] += pos
                gt_upleft+=[pop_gt_upleft,itme2_upleft]
         
        #무게 포함
        #mdd_w=np.random.uniform(low=5.0, high=18.0, size=N_mdd)
        #X_input=[list(a[0] + [a[1]]) for a in zip(X_input,mdd_w)]
        
        #순서 -> 랜덤 정렬
        #z = list(zip(X_input, gt_upleft))
        #shuffle(z)
        #X_input, gt_upleft = zip(*z)
        
        #순서 -> 크기순 정렬
        #s=[i*j*q for i,j,q in X_input]
        #s_idx=sorted(range(len(s)), key=lambda k: s[k])
        #X_input=np.array(X_input)[list(reversed(s_idx))]
        #gt_upleft=np.array(gt_upleft)[list(reversed(s_idx))]
        
        epi_input.append(X_input)
        epi_gt_upleft.append(gt_upleft)
    return epi_input,epi_gt_upleft#np.array(X_input)#_input


# def cornel(upleft,bxl,bxb):
#     #upleft: list [X, X], bxl: length of box(row), bxb: breadth of box(column) 
#     return [upleft,[upleft[0]+bxl-1,upleft[1]],[upleft[0],upleft[1]+bxb-1],[upleft[0]+bxl-1,upleft[1]+bxb-1]]
def box_cornel(upleft,bxl,bxb):
    #중상자 내부의 점
    return [upleft,[upleft[0],upleft[1]+bxb-1],[upleft[0]+bxl-1,upleft[1]],[upleft[0]+bxl-1,upleft[1]+bxb-1]]

def cornel(upleft,bxl,bxb):
    #whole_upleft에서 중박스의 모서리를 입력 받으면 해당 모서리에 해당하는 4개의 위치 반환
    return [upleft,[upleft[0],upleft[1]+bxb],[upleft[0]+bxl,upleft[1]],[upleft[0]+bxl,upleft[1]+bxb]]

def whole_upleft(tl,tr,bl, br,bxl,bxb):
    #하나의 중박스의 각 모서리에서 모든 가능한 4개의 중상자 위치 -> 4개 위치 * 4개 모서리 = 16개의 위치 반환
    # tl:top-left[X,X], tr:top-right[X,X], br:bottom-right[X,X], bl:bottom-left [X,X]
    # bxl: length of box(row), bxb: breadth of box(column) 
    upleft_list=[]
    upleft_list += cornel(tl,-bxl,-bxb) # -l, -b
    upleft_list += cornel([tr[0],tr[1]-bxb+1],-bxl,+bxb) # -l, +b
    upleft_list += cornel([bl[0]-bxl+1,bl[1]],+bxl,-bxb) # +l, -b
    upleft_list += cornel([br[0]-bxl+1,br[1]-bxb+1],+bxl,+bxb) # +l, +b 
    return upleft_list

def next_state(state,upleft,bxl,bxb):
    # state: current continaer, upleft: upleft of new box, bxl: length of box(row), bxb: breadth of box(column)
    nx_state=state.copy()
    nx_state[upleft[0]:upleft[0]+bxl,upleft[1]:upleft[1]+bxb]=1
    return nx_state
    
# def feasible_location(state,whole_upleft_list,bxl,bxb):
#     # state: current container, w_upleft: whole upleft list, 
#     f_upleft=whole_upleft_list.copy()
#     #remove - outside the container
#     f_upleft = np.array(f_upleft)
#     f_upleft=f_upleft[((f_upleft[:,0]>=0) & (f_upleft[:,1]>=0) & (f_upleft[:,0]+bxl<=state.shape[0]) & (f_upleft[:,1]+bxb<=state.shape[1]))]
#     #remove - duplicated
#     new_array = [tuple(row) for row in f_upleft]
#     f_upleft = np.unique(new_array, axis=0)
#     #remove - height>=1
#     idx=[]
#     for i,j in  enumerate(f_upleft):
#         # print(np.sum(state[i:i+1,j:j+2]))
#         if np.sum(state[j[0]:j[0]+bxl,j[1]:j[1]+bxb]) >=1: idx.append(i)#f_upleft.remove([i,j])#del f_upleft[i]
#     f_upleft=np.delete(f_upleft,idx,axis=0)
#     #remove - 상이한 높이(보류)
#     return f_upleft

def feasible_location(state,whole_upleft_list,bxl,bxb,bxh=None,state_H=None,is2d=True):
    # state: current container, w_upleft: whole upleft list
    state_L=state.shape[0]
    state_B=state.shape[1]
    f_upleft=whole_upleft_list.copy()
    f_upleft = np.array(f_upleft)
    #remove - duplicated
    new_array = [tuple(row) for row in f_upleft]
    f_upleft = np.unique(new_array, axis=0)
    #remove - outside the container
    f_upleft=f_upleft[((f_upleft[:,0]>=0) & (f_upleft[:,1]>=0) & (f_upleft[:,0]+bxl<=state_L) & (f_upleft[:,1]+bxb<=state_B))]
    #remove - height problem
    idx=[]
    if is2d:
        #remove - height>=1
        for i,[j,k] in  enumerate(f_upleft):
            if np.sum(state[j:j+bxl,k:k+bxb]) >=1: idx.append(i)#f_upleft.remove([i,j])#del f_upleft[i]
    else:
        for i,[j,k] in enumerate(f_upleft):
            #remove - 상이한 높이 or box height+state height > container height
            if np.sum(state[j:j+bxl,k:k+bxb] != state[j,k] ) >= 1: idx.append(i)
            elif state[j,k]+bxh > state_H: idx.append(i)
    f_upleft=np.delete(f_upleft,idx,axis=0)
    return f_upleft

def action_options_list(f_upleft_list):#action -> encoding (400,)
    action_options=[]
    for i,j in f_upleft_list:
        action_option=np.zeros((20,20))
        action_option[i,j]=1
        action_options.append(action_option)
    return action_options


class Bpp3DEnv():#(gym.Env):
    #metadata = {'render.modes': ['human']}
    #
    def __init__(self):
        super(Bpp3DEnv, self).__init__()
        self.length=20
        self.breadth=20
        self.height=20
        self.container=np.zeros((self.length,self.breadth))
        
    def step(self, upleft,bxl,bxb,bxh):
        self.container[upleft[0]:upleft[0]+bxl,upleft[1]:upleft[1]+bxb] += bxh 
        return self.container
    
    def reset(self):
        self.container=np.zeros((self.length,self.breadth))
        
    #def render(self, mode='human'):
    #    pass#
    #def close(self):
    #    pass#
    
    def terminal_reward(self):
        return np.sum(self.container)/(self.length*self.breadth*self.height)
    
