import gymnasium as gym
from gymnasium import spaces
from game import *

class Catan(gym.envs):
    # Define the initialization function
    def __init__(self):
        # Define the action space
        
        
        # Define the observation space
        
        
        # Define the game
        self.game = Game(10)
        
        
        
    def _get_obs(self):
        # Get the observation
        return None
    
    def _get_info(self):
        # Get the info
        return None
    
    def _get_reward(self):
        # Get the reward
        return None
    
    def reset(self):
        # Reset the game
        
        # return the observation
        return self._get_obs()
    
    def step(self, action):
        # Take a step in the game
        return None
    