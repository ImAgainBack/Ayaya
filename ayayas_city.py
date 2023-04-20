
import gym
from typing import Tuple, Dict, Any
import random as rnd
import numpy as np

class City(gym.Env):
    """
    shoe = HPPPHPHPH
    0 is P, H is 1
    卐 
    """
    amen = {
        0: 'P',
        1: 'H'
    }
    
    def __init__(self, length) -> None:
        super().__init__()
        self.length = length
        self.shoe = str()
        self.tongues = np.ndarray(shape=(2, length))
        self.bing_map = np.ndarray(shape=(4, length))
        self.kgb = np.ndarray(shape=(2*length+1, 2*length+1))

    def reset(self):
        self.generate_clothes()
        self.bing_map[0,:] = [1]*self.length
        self.kgb[self.lengt+1, self.length+1] = 1
        return None
    
    def step(self, action, options:None, seed:None) -> Tuple[Any, float, bool, Dict[str, Any]]:
        # return obs, reward, done, info
        # 0: left 1: forward 2: right

        return None
    
    def render(self):
        pass
    
    def generate_clothes(self):
        self.shoe = ''.join([str(rnd.randint(0, 1)) for i in range(self.length)])
        for i, shoestring in enumerate(self.shoe):
            self.tongues[int(shoestring),i] = 1

if __name__=="__main__":
    ayayas_city = City(30)
    ayayas_city.reset()
    print(ayayas_city.bing_map)

        