from catanatron.models.player import Player, Color
from catanatron.models.actions import Action, ActionType
from catanatron.game import Game
from catanatron.json import GameEncoder
from observations import get_observations
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO
from utils import mask_fn, my_reward_function
from catanatron_gym.envs import CatanatronEnv
from sb3_contrib.common.maskable.utils import get_action_masks
import numpy as np
from stable_baselines3.common.vec_env import VecEnv

# from catanatron_gym.envs.catanatron_env import CatanatronEnv
EXPECTED_METHOD_NAME = "action_masks"

class PPO_Player(Player):
    def __init__(self, color, is_bot=True, model_path=''):
        super().__init__(color, is_bot)
        self.model_path = model_path
        self.config =  {
            "reward_function": my_reward_function,
        }
        self.model = None
        
    def decide(self, game: Game, playable_actions,env,obs,map_fn):
        '''
        
        '''
        env = ActionMasker(env, mask_fn) 
        # print('here?')
        if self.model == None:
            self.model = MaskablePPO.load(self.model_path, env=env)
        else:
            pass
        # print('or here?')
        if isinstance(env, VecEnv):
            action_masks = np.stack(env.env_method(EXPECTED_METHOD_NAME))   
        else:
            action_masks = getattr(env, EXPECTED_METHOD_NAME)()
        # print('maybe here?')
        # print(env)
        # print(env.observation_space)
        # print(type(action_masks))
        # for i in action_masks:
        #     action_masks[i] = False
            
        # print(playable_actions)
        # for a in playable_actions:
        #     print(a.value)
        #     action_masks[a.value] = True
        # # obs = env.observation_space
        # print(obs)
        # print('surely not here?')
        actions, _states = self.model.predict(obs, action_masks=action_masks)
        # print('or not')
        # print(actions)
        # print(game.state.playable_actions)
        chosen_action = map_fn(actions, playable_actions)
        # print(chosen_action)
        # for a in playable_actions:
        #     if a.value == actions:
        #         return a
        
        return chosen_action
        

# %%

# %%