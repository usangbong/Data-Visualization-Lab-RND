import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class BppEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    #
    def __init__(self):
        super(BppEnv, self).__init__()
        self.container=np.zeros((20,20))
        
    def step(self, upleft,bxl,bxb):
        self.container[upleft[0]:upleft[0]+bxl,upleft[1]:upleft[1]+bxb]=1  
        return self.container
    
    def reset(self):
        self.container=np.zeros((20,20))
        
    def render(self, mode='human'):
        pass#
    def close(self):
        pass#
    
    def terminal_reward(self):
        return np.sum(self.container)/(20*20)