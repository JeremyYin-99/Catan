import gym 
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete 
import numpy as np
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
from catanatron import Game
from observations import get_observations, get_state
from catanatron.json import GameEncoder
import numpy as np


def play_action(action):
    return action
class CatanEnv(Env):
    def __init__(self,game:Game, players) -> None:
        super().__init__()
        self.game = game
        self.original_game = self.game.copy()
        self.players = players
        
        self.state = get_state(GameEncoder().default(self.game),self.players)
        
        self.observation_space = get_observations(GameEncoder().default(self.game), self.players[self.game.state.current_player_index], self.players)
        self.action_space = []
        for i in self.players:
            self.action_space.append(Discrete(len(self.game.state.playable_actions)))
        
        print(type(self.observation_space))
        print(self.observation_space)
        pass
    
    def step(self, action):
        self.game = self.game.execute(action=action)
        
        self.observation_space = get_observations(GameEncoder().default(self.game), self.players[self.game.state.current_player_index], self.players)
        
        self.action_space = Discrete(len(self.game.state.playable_actions))
        
        reward = 0
        
        if self.game.state.playable_actions[action].action_type.value == 'BUILD_SETTLEMENT':
            reward = 10
        elif self.game.state.playable_actions[action].action_type.value == 'BUILD_CITY':
            reward = 10
            
        if self.game.winning_color() != None:
            reward += 100
            done = True
        else:
            done = False
            
        self.state = get_state(GameEncoder().default(self.game),self.players)
        info = {}
        
        return self.state, reward, done, info
        pass
    
    def reset(self):
        self.game = self.original_game
        self.state = get_state(GameEncoder().default(self.game),self.players)
        self.action_space = Discrete(len(self.game.state.playable_actions))
        return self.state
        
        pass
    
