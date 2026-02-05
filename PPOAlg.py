import os
from environment import DrivingEnv
import matplotlib.pyplot as plt

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import plot_results
from stable_baselines3.common import results_plotter

log_dir = "tmp/"
os.makedirs(log_dir, exist_ok=True)

ckpt_dir = "checkpoints/"
os.makedirs(ckpt_dir, exist_ok=True)

env = DrivingEnv()
env = Monitor(env, log_dir)

model = PPO("MlpPolicy", env, verbose=1)
checkpoint_callback = CheckpointCallback(save_freq=500_000, save_path=ckpt_dir,
										 name_prefix='ppo_driving')

total_timesteps = 5_000_000
model.learn(total_timesteps=total_timesteps, callback=checkpoint_callback)

model.save("ppo_driving_model_final")
print("Final model saved as 'ppo_driving_model_final.zip'")

plot_results([log_dir], total_timesteps, results_plotter.X_TIMESTEPS, "PPO DrivingEnv")
plt.show()