# The goal of this script is to create a game of Catan playable by an artificial agent
import random
import numpy as np
from helper_dicts import *
from board import *
from actions import *
from player import *
from pprint import pprint

        

# Define the game
class Game:
    # Initialize the game taking into account the number of VPs needed to win
    def __init__(self, num_VPs, iterations = 50, number_of_players=2):
        self.num_VPs = num_VPs
        self.board = Board(number_of_players)
        self.turns = 1
        self.dice_roll = 0
        self.game_over = False
        self.winner = None
        self.has_rolled = False
        self.iterations = iterations # Don't need this if action masking is applied
        
        # set up check to see if the game is in the setup phase
        self.board.setup_phase = True
        
        # randomly assign the turn order
        random.shuffle(self.board.players)
    
    # define the function to take a step in the game
    def step(self):
        if self.winner is not None:
            return self.winner
        # if the turn is less than 8, the game is in the setup phase otherwise the game is in the normal phase
        if self.turns > 2*len(self.board.players):
            self.board.setup_phase = False
        
        # if the turn is 1, 2, 3, or 4, the game goes in order of the turn order. If the turn is 5, 6, 7, or 8, the game goes in reverse order of the turn order. If the turn is greater than 8, the game goes in order of the turn order.
        if self.turns < 1+len(self.board.players):
            player_turn = self.board.players[self.turns-1]
        elif self.turns < 1+2*len(self.board.players):
            player_turn = self.board.players[8-self.turns]
        else:
            player_turn = self.board.players[(self.turns-1)%4]        
        
        print(player_turn.player_num)
        # do the action for the player defined by player_turn
        # while the action is not end turn, keep taking actions
        # if the it is the setup phase, the player can only build 1 settlement and 1 road
        if self.board.setup_phase:
            action = Action(player_turn.player_num, self.board)
            mask = action.get_settlement_set_up_mask()
            action_id = player_turn.take_action(mask)
            boolean, action_type = action.make_move(action_id)
            assert boolean, "The action was not valid"
            
            action = Action(player_turn.player_num, self.board)
            mask = action.get_road_set_up_mask()
            action_id = player_turn.take_action(mask)
            boolean, action_type = action.make_move(action_id)
            assert boolean, "The action was not valid"
            
            self.turns += 1
            return True
            
        
        for i in range(self.iterations):
            action = Action(player_turn.player_num, self.board)
            mask = action.get_action_mask()
            action_id = player_turn.take_action(mask)
            
            # make the move
            boolean, action_type = action.make_move(action_id)
            assert boolean, "The action was not valid"
            
            # check if action is discarding cards
            if action_type == "Discard cards":
                for player in self.board.players:
                    discard_mask = action.get_discard_mask(player)
                    action_id = player.take_action(discard_mask)
                continue
            
            if action_type == "Road building":
                for i in range(2):
                    action = Action(player_turn.player_num, self.board)
                    mask = action.get_road_building_action_mask()
                    action_id = player_turn.take_action(mask)
                    boolean, action_type = action.make_move(action_id)
                    assert boolean, "The action was not valid"
                continue
            
            # check if action is ending turn
            if action_type == "End turn":
                break
            
        # increment the turn
        self.turns += 1
        