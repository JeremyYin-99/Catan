# %%
import os
from catanatron.models.player import Color
from catanatron_gym.envs import CatanatronEnv
from catanatron.players.weighted_random import WeightedRandomPlayer
import gym
import numpy as np
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks
from utils import *#mask_fn, my_reward_function
from PPO import PPO_Player

# %%
PPO_path = os.path.join('Training', 'Saved Models', 'PPO_model_5')
log_path = os.path.join('Training','Logs','First Attempts')

p1 = os.path.join('Training', 'Saved Models', 'PPO_model_2')
p2 = os.path.join('Training', 'Saved Models', 'PPO_model_3')
p3 = os.path.join('Training', 'Saved Models', 'PPO_model_4')
config = {
    "enemies": [PPO_Player(Color.RED,True,p1),
                PPO_Player(Color.ORANGE,True,p2),
                PPO_Player(Color.WHITE,True,p3)],
    "reward_function": my_reward_function,
}

# %%
#### attempt to train
# log_path = os.path.join('Training','Logs')
# players = [
#    SimplePlayer(Color.RED),
#    SimplePlayer(Color.BLUE),
#    SimplePlayer(Color.WHITE),
#    SimplePlayer(Color.ORANGE),
# ]
# game = Game(players)

# # env = CatanEnv(game=game,players=players)
# # model = PPO('MlpPolicy',env,verbose=1,tensorboard_log=log_path)
# # model.learn(total_timesteps=10000)
# config = {
#     "enemies": [WeightedRandomPlayer(Color.RED),
#                 WeightedRandomPlayer(Color.BLUE),
#                 WeightedRandomPlayer(Color.WHITE)]
# }
# env = CatanatronEnv(config=config)
# model = PPO('MlpPolicy',env,verbose=1,tensorboard_log=log_path)
# model.learn(total_timesteps=5000)

# %%

# import os
# from catanatron.game import Game
# from catanatron.models.actions import ActionType
# from catanatron.models.player import Color
# from catanatron_gym.envs import CatanatronEnv
# from catanatron.players.weighted_random import WeightedRandomPlayer
# import gym
# import numpy as np
# from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
# from sb3_contrib.common.wrappers import ActionMasker
# from sb3_contrib.ppo_mask import MaskablePPO



# Init Environment and Model
env = CatanatronEnv(config=config)
env = ActionMasker(env, mask_fn)  # Wrap to enable masking
# model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1,tensorboard_log=log_path)
model = MaskablePPO.load(PPO_path, env=env)

# Train
model.learn(total_timesteps=1_000_000)
model.save(PPO_path)

## %%
# from catanatron_gym.envs import CatanatronEnv
# import gym
# # env = CatanatronEnv(config=config) # try for different environments
# # env = ActionMasker(env, mask_fn)
# observation = env.reset()
# for t in range(100):
#         action = env.action_space.sample()
#         observation, reward, done, info = env.step(action)
#         print((observation, reward, done, info))
#         if done:
#             print("Finished after {} timesteps".format(t+1))
#             break
        

# %%
from stable_baselines3.common.evaluation import evaluate_policy


config = {
    "enemies": [WeightedRandomPlayer(Color.RED),
                WeightedRandomPlayer(Color.ORANGE),
                WeightedRandomPlayer(Color.WHITE)],
    "reward_function": my_reward_function,
}
p3 = os.path.join('Training', 'Saved Models', 'PPO_model_3')
config = {
    "enemies": [PPO_Player(Color.RED,True,p3),
                PPO_Player(Color.ORANGE,True,p3),
                PPO_Player(Color.WHITE,True,p3)],
    "reward_function": my_reward_function,
}

PPO_path = os.path.join('Training', 'Saved Models', 'PPO_model_5')
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
