"""
Visualize the trained PPO agent driving in the environment.
"""
import os
from environment import DrivingEnv
from stable_baselines3 import PPO

env = DrivingEnv(render_mode="human")

def run_visualization(model_path):
    if not os.path.exists(model_path):
        print(f"Checkpoint {model_path} not found")
        return
    
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
    
    print(f"{model_path} == Steps: {steps}, Total Reward: {checkpoint_reward:.2f}")


# # Visualize all checkpoints in the "checkpoints" directory
# for checkpoint in sorted(os.listdir("checkpoints")):
#     if checkpoint.endswith(".zip"):
#         run_visualization(os.path.join("checkpoints", checkpoint))

# Visualize the final trained model
final_model_path = "ppo_driving_model_final.zip"
run_visualization(final_model_path)
    

env.close()
print("Visualization complete!")
