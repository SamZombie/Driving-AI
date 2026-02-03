import gymnasium as gym
import numpy as np
import basegame
import pygame

class DrivingEnv(gym.Env):
    """
    Driving AI Environment compatible with Stable Baselines3.
    
    Action space: Discrete(5)
    - 0: turn left
    - 1: go straight
    - 2: turn right
    - 3: turn left + forward
    - 4: turn right + forward
    
    Observation space: Box(5,) - 5 sensor readings
    """
    
    metadata = {"render_modes": ["human", None], "render_fps": 60}

    def __init__(self, render_mode=None):
        self.game = basegame.Game()
        self.car = basegame.Car()
        self.display = None
        self.render_mode = render_mode
        
        self.observation_space = gym.spaces.Box(
            low=0, high=400, shape=(6,), dtype=np.float32
        )
        
        self.action_space = gym.spaces.Discrete(7)
        
        self._step_count = 0
        self.max_episode_steps = 1000
        self._last_points = 0
        
        if render_mode == "human":
            self.display = basegame.DisplayGame(init_pygame=True)
    
    def _get_observation(self):
        """Get sensor data as observation."""
        sensor_data = self.game.get_sensor_data(self.car)
        return np.array(sensor_data, dtype=np.float32)
    
    def _apply_action(self, action):
        """Apply action to the car."""
        if action == 0:  # turn left
            self.car.turn_left()
            self.car.stop()
        elif action == 1:  # go straight
            self.car.forward()
        elif action == 2:  # turn right
            self.car.turn_right()
            self.car.stop()
        elif action == 3:  # turn left + forward
            self.car.turn_left()
            self.car.forward()
        elif action == 4:  # turn right + forward
            self.car.turn_right()
            self.car.forward()
        elif action == 5:  # backward
            self.car.backward()
        elif action == 6:  # stop
            self.car.stop()
    
    def _compute_reward(self):
        """Compute reward for current step."""
        reward = 0
        
        current_points = self.car.points
        if current_points > self._last_points:
            reward += 10.0 * (current_points - self._last_points)
            self._last_points = current_points
        
        reward -= 0.01
        
        if self.game.point_out_of_bounds(self.car.pos[0], self.car.pos[1]):
            reward -= 5.0
        
        return float(reward)
    
    def reset(self, seed=None, options=None):
        """Reset the environment."""
        super().reset(seed=seed)
        
        self.game = basegame.Game()
        self.car = basegame.Car()
        self._step_count = 0
        self._last_points = 0
        
        if self.render_mode == "human" and self.display is None:
            self.display = basegame.DisplayGame(init_pygame=True)
        
        obs = self._get_observation()
        info = {}
        
        return obs, info
    
    def step(self, action):
        """Execute one step in the environment."""
       
        self._apply_action(action)
        self.car.move()
        self.game.check_gates(self.car)
        
        obs = self._get_observation()
        reward = self._compute_reward()
        
        terminated = False
        truncated = False
        info = {}
        
        if self.game.point_out_of_bounds(self.car.pos[0], self.car.pos[1]):
            terminated = True
            info["terminal_observation"] = obs
            self.game.on_death(self.car)
        
        self._step_count += 1
        if self._step_count >= self.max_episode_steps:
            truncated = True
        
        if self.render_mode == "human":
            self.render()
        
        return obs, reward, terminated, truncated, info
    
    def render(self):
        """Render the environment."""
        if self.render_mode == "human":
            if self.display is None:
                self.display = basegame.DisplayGame(init_pygame=True)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()

            self.game.clock.tick(60)
            self.display.draw_scene(self.game, self.car)
    
    def close(self):
        """Close the environment and cleanup resources."""
        if self.display is not None:
            pygame.quit()
            self.display = None


if __name__ == "__main__":    
    env = DrivingEnv(render_mode="human")
    obs, info = env.reset()

    for n in range(500):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

        if n % 10 == 0:
            print(f"Step {n}: Reward: {reward:.2f}, Points: {env.car.points}, Action: {action}")

        if terminated or truncated:
            obs, info = env.reset()
            print("Episode reset")
    
    env.close()
    print("Test completed")
