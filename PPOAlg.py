import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from environment import DrivingEnv

env = make_vec_env(DrivingEnv, n_envs=4)
model = PPO("MlpPolicy", env)
model.learn(100000)  