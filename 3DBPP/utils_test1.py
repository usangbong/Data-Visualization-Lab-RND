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
    #np.random.seed(seed=100)
    epi_input=[]
    epi_gt_upleft=[]
    
    for i in range(N_epi):
        N_mdd=np.random.choice(list(range(20,25)), 1)
        
        #X_input=[[c_l,c_b]]
        #gt_upleft=[[0,0]]
        X_input=[[int(c_l/2),int(c_b/2)]]*4
        gt_upleft=[[0,0],[int(c_l/2),0],[0,int(c_b/2)],[int(c_l/2),int(c_b/2)]]
        N_mdd-=4
        
        while(len(X_input)<N_mdd):
            idx=np.random.choice(list(range(len(X_input))), 1)[0]#pop an item randomly from X_input
            pop_item=X_input.pop(idx)#[l, b]
            pop_gt_upleft=gt_upleft.pop(idx)
            idx=np.random.choice([0,1],1)[0]#choose an axis randomly
            
            if pop_item[idx]<=3:#if pop_item[idx]==1:
                X_input.append(pop_item)
                gt_upleft.append(pop_gt_upleft)
            else:#item split
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
        
        #순서 -> 랜덤 정렬
        #z = list(zip(X_input, gt_upleft))
        #shuffle(z)
        #X_input, gt_upleft = zip(*z)
        
        #순서 -> 크기순 정렬
        s=[i*j for i,j in X_input]
        s_idx=sorted(range(len(s)), key=lambda k: s[k])
        X_input=np.array(X_input)[list(reversed(s_idx))]
        gt_upleft=np.array(gt_upleft)[list(reversed(s_idx))]
                
        epi_input.append(X_input)
        epi_gt_upleft.append(gt_upleft)
    return epi_input,epi_gt_upleft


def generation_3dbox(N_epi=1,c_l=20,c_b=20,c_h=20):
    #c_l, c_b, c_h: length, breadth, height
    #np.random.seed(seed=100)
    epi_input=[]
    epi_gt_upleft=[]
    
    for i in range(N_epi):
        N_mdd=np.random.choice(list(range(20,25)), 1)
        
        #X_input=[[c_l,c_b,c_h]]
        #gt_upleft=[[0,0,0]]
        X_input=[[int(c_l/2),int(c_b/2),int(c_h/2)]]*8
        gt_upleft=[[0,0,0],[int(c_l/2),0,0],[0,int(c_b/2),0],[int(c_l/2),int(c_b/2),0],
                  [0,0,int(c_h/2)],[int(c_l/2),0,int(c_h/2)],[0,int(c_b/2),int(c_h/2)],[int(c_l/2),int(c_b/2),int(c_h/2)]]
        N_mdd-=8
        
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
        s=[i*j*q for i,j,q in X_input]
        s_idx=sorted(range(len(s)), key=lambda k: s[k])
        X_input=np.array(X_input)[list(reversed(s_idx))]
        gt_upleft=np.array(gt_upleft)[list(reversed(s_idx))]
        
        epi_input.append(X_input)
        epi_gt_upleft.append(gt_upleft)
    return epi_input,epi_gt_upleft#np.array(X_input)#_input
