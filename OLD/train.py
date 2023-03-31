# %%
import os
from stable_baselines3.common.evaluation import evaluate_policy
from catanatron.models.player import Color
from catanatron_gym.envs import CatanatronEnv
from catanatron.players.weighted_random import WeightedRandomPlayer
import gym
import numpy as np
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks
from utils import *
from PPO import PPO_Player
weighted_player = False
# %%
PPO_path = os.path.join('Training', 'SelfPlay Models', 'PPO_model_Weight_Player_Destroyer_1')
log_path = os.path.join('Training','Logs','Weighted_Agent')

weighted_player = True

if weighted_player == False:
    p1 = os.path.join('Training', 'Saved Models', 'PPO_model_2')
    p2 = os.path.join('Training', 'Saved Models', 'PPO_model_3')
    p3 = os.path.join('Training', 'Saved Models', 'PPO_model_4')
    config = {
        "enemies": [PPO_Player(Color.RED,True,p1),
                    PPO_Player(Color.ORANGE,True,p2),
                    PPO_Player(Color.WHITE,True,p3)],
        "reward_function": my_reward_function,
    }
else:
    config = {
    "enemies": [WeightedRandomPlayer(Color.RED),
                WeightedRandomPlayer(Color.ORANGE),
                WeightedRandomPlayer(Color.WHITE)],
    "reward_function": my_reward_function,
    }
    

# %%


# Init Environment and Model
env = CatanatronEnv(config=config)
env = ActionMasker(env, mask_fn)  # Wrap to enable masking
model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1,tensorboard_log=log_path)
# model = MaskablePPO.load(PPO_path, env=env)

# Train
model.learn(total_timesteps=5_000_000)
model.save(PPO_path)


# %%

# config = {
#     "enemies": [WeightedRandomPlayer(Color.RED),
#                 WeightedRandomPlayer(Color.ORANGE),
#                 WeightedRandomPlayer(Color.WHITE)],
#     "reward_function": my_reward_function,
# }

if weighted_player == False:
    p3 = os.path.join('Training', 'Saved Models', 'PPO_model_3')
    p3 = 'Training/Saved Models/PPO_model_Weight_Player_Destroyer'
    p3 = 'Training/SelfPlay Models/Current/PPO_Model_100'
    config = {
        "enemies": [PPO_Player(Color.RED,True,p3),
                    PPO_Player(Color.ORANGE,True,p3),
                    PPO_Player(Color.WHITE,True,p3)],
        "reward_function": my_reward_function,
    }

    PPO_path = os.path.join('Training', 'Saved Models', 'PPO_model_5')
    
    
# %%
p3 = 'Training/SelfPlay Models/Current/PPO_Model'
PPO_path = 'Training/Saved Models/PPO_model_Weight_Player_Destroyer'
# PPO_path = 'Training/SelfPlay Models/Current_1/PPO_Model_100'
# PPO_path = 'Training/SelfPlay Models/Current/PPO_Model'
config = {
        "enemies": [PPO_Player(Color.RED,True,p3),
                    PPO_Player(Color.ORANGE,True,p3),
                    PPO_Player(Color.WHITE,True,p3)],
        "reward_function": my_reward_function,
    }


env = CatanatronEnv(config=config)
env = ActionMasker(env, mask_fn)  # Wrap to enable masking
model = MaskablePPO.load(PPO_path, env=env)
episodes = 500
wins = 0
for i in range(episodes):
    obs = env.reset()
    done = False
    while done == False:
        action_masks = get_action_masks(env)
        actions, _states = model.predict(obs, action_masks=action_masks)
        
        obs, rewards, done, info = env.step(actions)
        # print(obs)
        
        if done == True:
            # print(info)
            if rewards >= WIN_REWARD:
                wins +=1
print(wins)
print(wins/episodes)
# %%
