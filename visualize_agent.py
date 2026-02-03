"""
Visualize the trained PPO agent driving in the environment.
"""
import os
from environment import DrivingEnv
from stable_baselines3 import PPO

env = DrivingEnv(render_mode="human")

for checkpoint in range(100_000, 1_200_000, 100_000):
    model_path = os.path.join("checkpoints", f"ppo_driving_{checkpoint}_steps.zip")
    if not os.path.exists(model_path):
        print(f"Checkpoint {model_path} not found, playing final...")
        model_path = "ppo_driving_model_final.zip"
        if not os.path.exists(model_path):
            print("Final model not found, skipping...")
            continue
    
    print(f"Loading model from {model_path}...")
    model = PPO.load(model_path)
    obs, info = env.reset()
    checkpoint_reward = 0
    steps = 0
    
    done = False
    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        checkpoint_reward += reward
        steps += 1
        done = terminated or truncated
    
    print(f"Checkpoint {checkpoint}: Steps: {steps}, Total Reward: {checkpoint_reward:.2f}")

env.close()
print("Visualization complete!")
