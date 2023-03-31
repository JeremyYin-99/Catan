import numpy as np
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks
from catanatron.game import Game
from catanatron.models.actions import ActionType

WIN_REWARD = 500
LOSE_REWARD = 500

def mask_fn(env, aug = None) -> np.ndarray:
    if aug == None:
        valid_actions = env.get_valid_actions()
        mask = np.zeros(env.action_space.n, dtype=np.float32)
        mask[valid_actions] = 1
    else:
        valid_actions = aug
        mask = np.zeros(env.action_space.n, dtype=np.float32)
        mask[valid_actions] = 1
    # print(mask)

    return np.array([bool(i) for i in mask])


def my_reward_function(game:Game, p0_color, catan_action):
    winning_color = game.winning_color()
    reward = 0#current_reward
    # print(catan_action.action_type)
    # print(catan_action.action_type == ActionType.BUILD_ROAD)
    # print(catan_action.action_type == ActionType.BUILD_SETTLEMENT)
    # print(catan_action.action_type == ActionType.BUILD_CITY)
    
    if catan_action.action_type == ActionType.BUILD_ROAD:
        return reward + 1
    elif catan_action.action_type == ActionType.BUILD_SETTLEMENT:
        reward += 20
    elif catan_action.action_type == ActionType.BUILD_CITY:
        reward += 10
        
    if p0_color == winning_color:
        print('player actually won')
        return reward + WIN_REWARD
    elif winning_color is None:
        return reward
    else:
        print('player lost... :(')
        return reward-LOSE_REWARD