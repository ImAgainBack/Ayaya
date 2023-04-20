import gym
import numpy as np
import random as rnd
from typing import Tuple
from gym.core import ObsType, ActType


class GridEnv(gym.Env):
    """
    On va tout écrire en français
    en fait non
    """

    def __init__(self, length) -> None:
        super().__init__()
        # Core
        self.length = length

        # Static - Core
        self.sequence_str = str()
        self.sequence_1hot = np.ndarray(shape=(2, length))
        
        # Dynamic -
        # Core
        self.saw_array = np.ndarray(shape=(2*length+1, 2*length+1))
        self.saw_1hot = np.ndarray(shape=(4, length))
        # Auxiliary
        self.step_counter = int()
        self.ayaya = tuple()
        self.behind_ayaya = tuple()

    def reset(self, seed=None, options=None) -> Tuple[ObsType, dict]:
        # TODO: add generate random sequence
        
        self.saw_1hot[0,:] = [1]*self.length
        self.saw_array[self.length+1,self.length+1] = 1
        self.step_counter = 1

        # TODO: add the OOL start

        return None
    
    def step(self, action: ActType) -> Tuple[ObsType, float, bool, bool, dict]:
        direction = self.ayaya - self.behind_ayaya
        match action:
            case 0: # LEFT
                direction = (-direction[1], direction[0])
            case 1:
                pass
            case 2:
                direction = (direction[1], -direction[0])

        self.behind_ayaya = self.ayaya
        self.ayaya = self.ayaya + direction

        self.step_counter += 1
        self.saw_array[self.ayaya] = self.step_counter
        self.saw_1hot[action+1, self.step_counter] = 1
        self.saw_1hot[0, self.step] = 0

        # TODO: copute reward

        return None 
    
    def render(self):
        return None
    
    def _generate_sequence(self):
        self.sequence_str = ''.join([str(rnd.randint(0, 1)) for i in range(self.length)])
        for i, unit in enumerate(self.sequence_str):
            self.sequence_1hot[int(unit), i] = 1
