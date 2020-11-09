import numpy as np

def generationg_input(N_epi=1):
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