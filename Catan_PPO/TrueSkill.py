# %%
from catanatron.models.player import Color
from catanatron_gym.envs import CatanatronEnv
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO
from PPO import PPO_Player
from utils import *
import matplotlib.pyplot as plt
import numpy as np
import random
import os

# %%
true_skill_diff_better = []

folder = 'Training/SelfPlay Models/Challengers'
dir = os.listdir(folder)
dir.remove('.DS_Store')

mapping = []

for i in dir:
    num = i.split('_')[-1]
    num = num.split('.')[0]
    num = int(num)
    mapping.append(num)

for m in range(len(mapping[1:])):
    count = 0
    for element in mapping:
        if element==m:
            opponent_path = folder+'/'+dir[count][:-4]
        elif element==m+1:
            challenger_path = folder+'/'+dir[count][:-4]
        count +=1
    
    print(opponent_path)
    print(challenger_path)
    config = {
            "enemies": [PPO_Player(Color.RED,True,opponent_path),
                        PPO_Player(Color.ORANGE,True,opponent_path),
                        PPO_Player(Color.WHITE,True,opponent_path)],
            "reward_function": my_reward_function,
    }
    env = CatanatronEnv(config=config)
    env = ActionMasker(env, mask_fn)  # Wrap to enable masking
    model = MaskablePPO.load(challenger_path, env=env)
    
    episodes = 1000
    wins = 0
    for e in range(episodes):
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
    true_skill_diff_better.append(wins/episodes)

# %%

fig, ax = plt.subplots()
ax.plot(true_skill_diff_better)
ax.set_xlabel('Iteration')
ax.set_ylabel('Win-Rate')
ax.set_title('Win-Rate of Each Iteration vs the Previous Iteration')
fig.savefig('WinRate_Better_Model.png')
fig.show()
# %%
