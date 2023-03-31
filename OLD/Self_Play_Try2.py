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
import random


# %%
log_path = os.path.join('Training','SelfPlay Models','Logs')
PPO_Path = 'Training/SelfPlay Models/Current/PPO_Model'

config = {
        "enemies": [WeightedRandomPlayer(Color.RED),
                    WeightedRandomPlayer(Color.ORANGE),
                    WeightedRandomPlayer(Color.WHITE)],
        "reward_function": my_reward_function,
    }
env = CatanatronEnv(config=config)
env = ActionMasker(env, mask_fn)  # Wrap to enable masking
model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1,tensorboard_log=log_path)
model.learn(total_timesteps=50_000)
model.save("Training/SelfPlay Models/Challengers/PPO_Model_{}".format(0))

episodes = 500
start = len(os.listdir("Training/SelfPlay Models/Current"))
for i in range(episodes):
    files = os.listdir("Training/SelfPlay Models/Challengers")
    weights = list(np.linspace(1,len(files),len(files),dtype = int))
    for i in range(len(weights)):
        weights[i] = weights[i]**4
    challenger1 = 'Training/SelfPlay Models/Challengers/{}'.format(random.choices(files, weights=weights, k=1)[0][:-4])
    challenger2 = 'Training/SelfPlay Models/Challengers/{}'.format(random.choices(files, weights=weights, k=1)[0][:-4])
    challenger3 = 'Training/SelfPlay Models/Challengers/{}'.format(random.choices(files, weights=weights, k=1)[0][:-4])
    
    print('challenger1')
    print(challenger1)
    print('challenger2')
    print(challenger2)
    print('challenger3')
    print(challenger3)
    
    config = {
        "enemies": [PPO_Player(Color.RED,True,challenger1),
                    PPO_Player(Color.ORANGE,True,challenger2),
                    PPO_Player(Color.WHITE,True,challenger3)],
        "reward_function": my_reward_function,
    }
    # Init Environment and Model
    env = CatanatronEnv(config=config)
    env = ActionMasker(env, mask_fn)  # Wrap to enable masking
    try:
        model = MaskablePPO.load(PPO_Path, env=env)
    except:
        print('Training the original model')
        model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1,tensorboard_log=log_path)

    # Train
    model.learn(total_timesteps=50_000)
    model.save(PPO_Path)
    model.save("Training/SelfPlay Models/Challengers/PPO_Model_{}".format(i))
    