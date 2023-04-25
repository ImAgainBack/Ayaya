import gym
import registration
import envs
from envs.d2_grid_env import GridEnv
from sb3_contrib import RecurrentPPO
from gym import envs
import os 
from stable_baselines3.common.callbacks import BaseCallback
import json
from collections import defaultdict


def saw_training(env, folder='auto', run_name='default', save_interval=100_000, depth_field=1, length=14, render_mode=None, total_timesteps=1_000_000, **kwargs):
    params = {
        "learning_rate": 1e-3,
        "n_steps": 128,
        "batch_size": 128,
        "n_epochs": 10,
        "gamma": 0.99,
        "gae_lambda": 0.95,
        "clip_range": 0.2,
        "clip_range_vf": None,
        "normalize_advantage": True,
        "ent_coef": 0.0,
        "vf_coef": 0.5,
        "max_grad_norm": 0.5,
        "use_sde": False,
        "sde_sample_freq": -1,
        "target_kl": None,
        "verbose": 1,
        # Add other stuff, idk
    }
    
    model_save_path = f'./models/{folder}/{run_name}'
    env = gym.make(env, length=length)
    model = RecurrentPPO("MlpLstmPolicy", env, tensorboard_log=f'./logs/{folder}/{run_name}', **params)
    model.learn(
        total_timesteps=total_timesteps,
    )
    
    model.save(model_save_path)  

if __name__=='__main__':
    #folder = str(input("What is the type of the test? "))
    #run_name = str(input("What is the name of the run? "))
    #saw_training('SAW-v0', folder, run_name)

    folder = "test"
    run_name = "test"
    saw_training('ayaya-v0', folder, run_name)