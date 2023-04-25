import gym
from envs.d2_grid_env import GridEnv

gym.register(
    id="ayaya-v0",
    entry_point="envs.d2_grid_env:GridEnv"
)