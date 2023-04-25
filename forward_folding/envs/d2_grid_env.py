import gym
from gym import spaces
import numpy as np
import random as rnd
from typing import Tuple
# from gym.core import ObsType, ActType


class GridEnv(gym.Env):
    """
    On va tout écrire en français
    en fait non
    """
    amen = {
        '0': 'P',
        '1': 'H',
    }
    nema = {
        'P': 0,
        'H': 1,
    }

    def __init__(self, length) -> None:
        super().__init__()
        # Core
        self.length = length
        self.step_counter = 0

        # Static - Core
        self.sequence_str = str()
        self.sequence_1hot = np.ndarray(shape=(2, length))
        
        # Dynamic -
        # Core
        self.saw_array = np.ndarray(shape=(2*length+1, 2*length+1))
        self.saw_1hot = np.ndarray(shape=(4, length))
        # Auxiliary
        self.step_counter = int()
        self.ayaya = list()
        self.behind_ayaya = list()

        # Spaces
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,self.length))

    def reset(self, seed=None, options=None): #-> Tuple[ObsType, dict]:
        self._generate_sequence()
        self.saw_1hot[0,:] = [1]*self.length
        self.saw_array = np.zeros((2*self.length+1, 2*self.length+1), dtype=np.uint)
        self.step_counter = 0
        done = False

        # Place un 1 au milieu
        self.step_counter += 1
        self.saw_array[self.length+1,self.length+1] = self.step_counter
        

        # Place un 2 au dessus
        self.step_counter += 1
        self.saw_array[self.length,self.length+1] = self.step_counter
        self.ayaya = np.where(self.saw_array == 2)
        self.behind_ayaya = np.where(self.saw_array == 1)

        self.step(0)

        self.saw_array
        obs = self.get_obs()
        
        return obs
    
    def step(self, action): #-> Tuple[ObsType, float, bool, bool, dict]:
        direction = np.subtract(self.ayaya, self.behind_ayaya)
        match action:
            case 0: # LEFT
                direction = (-direction[1], direction[0])
            case 1:
                pass
            case 2:
                direction = (direction[1], -direction[0])

        self.behind_ayaya = self.ayaya
        self.ayaya = np.add(self.ayaya, direction)

        self.step_counter += 1
        if self.saw_array[self.ayaya[0], self.ayaya[1]] != 0:
            done = True
            reward = 0
            self.saw_array[self.ayaya[0], self.ayaya[1]] = self.step_counter
            self.saw_1hot[action+1, self.step_counter-1] = 1
            obs = self.get_obs()

            return obs, reward, done, {} 

        self.saw_1hot[0, self.step_counter-1] = 0
        self.saw_array[self.ayaya[0], self.ayaya[1]] = self.step_counter
        self.saw_1hot[action+1, self.step_counter-1] = 1
        done = (self.step_counter == self.length)
        # print(done)
        reward = abs(self.compute_reward(self.saw_array, self.sequence_str)) if done else 0
        if done: 
            print(reward)
        obs = self.get_obs()
        return obs, reward, done, {} 
    
    def render(self):
        return None
    
    def _generate_sequence(self):
        self.sequence_str = ''.join([self.amen[str(rnd.randint(0, 1))] for i in range(self.length)])
        for i, unit in enumerate(self.sequence_str):
            self.sequence_1hot[self.nema[unit], i] = 1

    @staticmethod
    def compute_reward(path, sequence):
        """ Match the sequence to each paths and compute the energy. Return all minimum energy structures. Stores paths in a heap.
        H-H bond = -1
        P-P bond = 0
        :param paths: list of paths that have been pre-computed by brute-force algorithm 
        :param sequence: the sequence to be folded
        :return: list of paths with minimum energy
        """

        # print(path)
        # print(sequence)
        H_coords_even = []
        H_coords_odd = []
        energy = 0
        j = 0  # tracks the last time we saw an H along the chain
        for i in range(len(sequence)):
            i += 1
            if sequence[i-1] == 'H':
                # Compute the energy of interaction with any Hs before it
                # curr_x, curr_y = path[i]
                curr_x, curr_y = np.where(path == i)
                if i == j + 1:  # that means that the last time we encountered an H, it was adjacent to the current H
                    if i % 2 == 0: #even
                        H_coords_even.append((curr_x, curr_y))
                        for coord in H_coords_odd[:-1]:  # skip last element
                            distance = abs(curr_x - coord[0]) + abs(curr_y - coord[1])  # calculate distance between 2 Hs using city block distance
                            if distance == 1:
                                energy -= 1
                    else: # odd
                        H_coords_odd.append((curr_x, curr_y))
                        for coord in H_coords_even[:-1]:  # skip last element
                            distance = (curr_x - coord[0]) ** 2 + (
                                    curr_y - coord[1]) ** 2  # calculate distance between 2 Hs
                            if distance == 1:
                                energy -= 1

                else:
                    if i % 2 == 0:
                        H_coords_even.append((curr_x, curr_y))
                        for coord in H_coords_odd:  # skip last element
                            distance = (curr_x - coord[0]) ** 2 + (
                                    curr_y - coord[1]) ** 2  # calculate distance between 2 Hs
                            if distance == 1:
                                energy -= 1
                    else:
                        H_coords_odd.append((curr_x, curr_y))
                        for coord in H_coords_even:  # skip last element
                            
                            distance = (curr_x[0] - coord[0]) ** 2 + (
                                    curr_y[0] - coord[1]) ** 2  # calculate distance between 2 Hs
                            if distance == 1:
                                energy -= 1
                j = i
        return energy


    def get_obs(self):
        obs = np.vstack([self.saw_1hot, self.sequence_1hot])
        return obs