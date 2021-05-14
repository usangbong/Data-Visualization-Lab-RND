import numpy as np
from random import shuffle
from itertools import chain, combinations
from itertools import compress

def powerset(iterable):
    subset_list = list(chain.from_iterable(combinations(iterable, r) for r in range(1,len(iterable)+1)))
    return [list(i) for i in subset_list]

def find_factor(n):
    factor_values = []
    for i in range(1, n + 1):
        if n % i == 0:
            factor_values.append(i)

    values = []
    for v in factor_values:
        values.append(v)

    return values[1:-1]

def divide_uniform(pop_item, position, axis_idx,n_div,is_factors=False):
    # 나뉜 size 계산
    if is_factors: size_list = [(pop_item[axis_idx])//n_div]*n_div
    else:    
        size_list = []
        for i in range(n_div-1):
            if i == 0 : size_list.append((pop_item[axis_idx])//(n_div-i))
            else: size_list.append((pop_item[axis_idx] - size_list[-1])//(n_div-i))
        size_list.append(pop_item[axis_idx] - np.sum(size_list))
    # size와 position 계산
    sizes, positions = [],[] 
    for i in range(n_div):
        #size
        item = pop_item.copy()
        item[axis_idx] = size_list[i]
        sizes.append(item)
        #position
        new_position = position.copy()
        if i!=0: new_position[axis_idx] += int(np.sum(size_list[:i]))
        positions.append(new_position)
    return sizes,positions

def divide_uniform_multi_axis(item_size, item_pos, axis_idx_list,n_div,is_factors=False):
    item_size = [item_size]; item_pos = [item_pos]
    for axis_idx in axis_idx_list:
        n=len(item_size)
        sizes,positions = [],[]
        for i in range(n):
            size = item_size.pop()
            pos = item_pos.pop()
            size, pos = divide_uniform(size, pos , axis_idx, n_div,is_factors)
            sizes += size
            positions += pos
        item_size = sizes.copy()
        item_pos = positions.copy()
    return sizes, positions

def generation_3dbox(case_size=[[20,20,20],[25,20,15]], N_mdd=20, min_s = 3, is_prediv=0):
    #c_l, c_b, c_h: length, breadth, height
    case_input=[]
    case_gt_upleft=[]
    for c_l,c_b,c_h in case_size:
        if type(N_mdd)==tuple: np.random.choice(list(range(N_mdd[0],N_mdd[1])), 1)#N_mdd = 20 # 
        X_input=[[c_l,c_b,c_h]]
        gt_upleft=[[0,0,0]]

        if is_prediv==8: #8분할
            X_input, gt_upleft = divide_uniform_multi_axis(X_input.pop(), gt_upleft.pop(), [0,1,2],2)
        elif is_prediv == 4:#4분할
            X_input, gt_upleft = divide_uniform_multi_axis(X_input.pop(), gt_upleft.pop(), [0,1],2)
        elif is_prediv == 'h': #높이 분할
            X_input, gt_upleft = divide_uniform_multi_axis(X_input.pop(), gt_upleft.pop(), [2],3)
        elif is_prediv == '4h':
            X_input, gt_upleft = divide_uniform_multi_axis(X_input.pop(), gt_upleft.pop(), [2],3)
            for i in range(3):
                sizes, positions = divide_uniform_multi_axis(X_input.pop(0), gt_upleft.pop(0), [0,1],2)
                X_input+=sizes;gt_upleft+=positions
        elif is_prediv == '2h':
            X_input, gt_upleft = divide_uniform_multi_axis(X_input.pop(), gt_upleft.pop(), [2],3)
            for i in range(3):
                sizes, positions = divide_uniform_multi_axis(X_input.pop(0), gt_upleft.pop(0), [0],2)
                X_input+=sizes;gt_upleft+=positions
                
        while(len(X_input)<N_mdd):
            idx=np.random.choice(range(len(X_input)), 1)[0]
            pop_item=X_input.pop(idx)#[l, b, h]
            pop_gt_upleft=gt_upleft.pop(idx)
            axis_idx = np.random.choice([0,1,2],1)[0]
            factors = find_factor(pop_item[axis_idx])
            factors = list(compress(factors, pop_item[axis_idx]/np.array(factors) >=3))
            if pop_item[axis_idx] < min_s*2 or len(factors)==0:
                X_input.append(pop_item)
                gt_upleft.append(pop_gt_upleft)
            else:
                n_div = np.random.choice(factors,1)[0]
                if False:
                    axis_idx_list = []
                    for i in range(3):
                        if pop_item[idx]==pop_item[i]: axis_idx_list.append(i)
                    axis_idx_list = powerset(axis_idx_list)
                    axis_idx_list =list(compress(axis_idx_list, [idx in i for i in axis_idx_list]))
                    axis_idx_list = axis_idx_list[np.random.choice(len(axis_idx_list),1)[0]]
                axis_idx_list = [axis_idx]
                #sizes, positions = divide_uniform_multi_axis(pop_item, pop_gt_upleft, axis_idx_list, n_div)
                #sizes, positions = divide_uniform(pop_item, pop_gt_upleft, idx, n_div)
                sizes, positions = divide_uniform_multi_axis(pop_item, pop_gt_upleft, axis_idx_list, n_div,is_factors=True)
                X_input+=sizes;gt_upleft+=positions
        #무게 포함
        #mdd_w=np.random.uniform(low=5.0, high=18.0, size=N_mdd)
        #X_input=[list(a[0] + [a[1]]) for a in zip(X_input,mdd_w)]

        #순서 -> 랜덤 정렬 (single)
        #z = list(zip(X_input, gt_upleft))
        #shuffle(z)
        #X_input, gt_upleft = zip(*z)
           
        #순서 -> 크기순 정렬
        #s=[i*j*q for i,j,q in X_input]
        #s_idx=sorted(range(len(s)), key=lambda k: s[k])
        #X_input=np.array(X_input)[list(reversed(s_idx))]
        #gt_upleft=np.array(gt_upleft)[list(reversed(s_idx))]

        #순서 -> 아래부터 정렬
        #idx = np.argsort(np.array(gt_upleft)[:,2])
        #gt_upleft = np.array(gt_upleft)[idx]
        #X_input = np.array(X_input)[idx]
        
        #순서 -> 1.아래 2.안쪽 3.왼쪽
        gt_upleft = np.array(gt_upleft)
        idx = np.lexsort((gt_upleft[:,1],gt_upleft[:,0],gt_upleft[:,2]))
        gt_upleft = gt_upleft[idx]
        X_input = np.array(X_input)[idx]
        
        case_input.append(X_input)
        case_gt_upleft.append(gt_upleft)
    return case_input,case_gt_upleft



def generation_3dbox_random(case_size=[[20,20,20],[25,20,15]],min_s = 3, is_prediv=0, N_mdd=22):
    #c_l, c_b, c_h: length, breadth, height
    #np.random.seed(seed=100)
    case_input=[]
    case_gt_upleft=[]
    
    for c_l,c_b,c_h in case_size:
        #N_mdd=22#12#np.random.choice(list(range(23,28)), 1)

        X_input=[[c_l,c_b,c_h]]
        gt_upleft=[[0,0,0]]
        
        if is_prediv==8: #8분할
            X_input, gt_upleft = divide_uniform_multi_axis(X_input.pop(), gt_upleft.pop(), [0,1,2],2)
            
        elif is_prediv == 4:#4분할
            X_input, gt_upleft = divide_uniform_multi_axis(X_input.pop(), gt_upleft.pop(), [0,1],2)
            
        elif is_prediv == 'h': #높이 분할
            X_input, gt_upleft = divide_uniform_multi_axis(X_input.pop(), gt_upleft.pop(), [2],3)
        
        while(len(X_input)<N_mdd):
            idx=np.random.choice(range(len(X_input)), 1)[0]#pop an item randomly from X_input
            pop_item=X_input.pop(idx)#[l, b, h]
            pop_gt_upleft=gt_upleft.pop(idx)
            idx=np.random.choice([0,1,2],1)[0]#choose an axis randomly
            if pop_item[idx] < min_s*2:
                X_input.append(pop_item)
                gt_upleft.append(pop_gt_upleft)
            else:#item split
                pos=np.random.choice(list(range(min_s,pop_item[idx]+1-min_s)),1)[0]#choose a position randomly - distance
                #item
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
        
        #순서 -> 아래부터 정렬
        #idx = np.argsort(np.array(gt_upleft)[:,2])
        #gt_upleft = np.array(gt_upleft)[idx]
        #X_input = np.array(X_input)[idx]
        
        #순서 -> 1.아래 2.안쪽 3.왼쪽
        gt_upleft = np.array(gt_upleft)
        idx = np.lexsort((gt_upleft[:,1],gt_upleft[:,0],gt_upleft[:,2]))
        gt_upleft = gt_upleft[idx]
        X_input = np.array(X_input)[idx]
        
        case_input.append(X_input)
        case_gt_upleft.append(gt_upleft)
    return case_input,case_gt_upleft


'''
X_input=[[int(c_l/2),int(c_b/2),int(c_h/2)]]*8
            gt_upleft=[[0,0,0],[int(c_l/2),0,0],[0,int(c_b/2),0],[int(c_l/2),int(c_b/2),0],
                      [0,0,int(c_h/2)],[int(c_l/2),0,int(c_h/2)],[0,int(c_b/2),int(c_h/2)],[int(c_l/2),int(c_b/2),int(c_h/2)]]
                      
X_input=[[int(c_l/2),int(c_b/2),int(c_h)]]*4
            gt_upleft=[[0,0,0],[int(c_l/2),0,0],[0,int(c_b/2),0],[int(c_l/2),int(c_b/2),0]]                      
h1,h2,h3 = c_h//3, c_h//3, c_h-2*(c_h//3)
            X_input=[[c_l,c_b,i] for i in [h1,h2,h3]]
            gt_upleft = [[0,0,0],[0,0,h1],[0,0,h1+h2]]
            N_mdd-=3
            for i in range(3):
                idx=np.random.choice([0,1],1)[0]
                pos= c_h//2
                item1 = X_input[i].copy();item2 = X_input[i].copy();
                item1[idx]=pos;item2[idx]=X_input[i][idx]-pos
                X_input+=[item1,item2]
                itme2_upleft=gt_upleft[i].copy()
                itme2_upleft[idx] += pos
                gt_upleft+=[gt_upleft[i],itme2_upleft]
            del X_input[:3], gt_upleft[:3]                      
'''