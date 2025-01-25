import random
# Define the players
class Player:
    def __init__(self, player_num):
        self.player_num = player_num
        self.settlements_available = 5
        self.cities_available = 4
        self.roads = 15
        self.resources = {"wool": 0, "lumber": 0, "grain": 0, "ore": 0, "brick": 0}
        self.dev_cards = {"knight": 0, "victory_point": 0, "monopoly": 0, "road_building": 0, "year_of_plenty": 0}
        self.longest_road = False
        self.largest_army = False
        self.victory_points = 0
        self.settlement_list = []
        self.road_list = []
        self.has_rolled = False
        self.settlements_available = 5
        self.cities_available = 4
        self.played_knights = 0

        self.road_building = 0
        self.can_play_development_card = True
        
        self.to_discard = 0
        self.to_build = 0

    def end_turn(self):
        self.has_rolled = False

        self.can_play_development_card = True

        self.road_building = 0
        
    # take an action
    def take_action(self, action_mask):
        # return the action_id
        act = [i for i in range(len(action_mask)) if action_mask[i] == 1][0]
        print(act)
        return act
    
    
class RandomPlayer(Player):
    def take_action(self, action_mask):
        # return the action_id
        return random.sample([i for i in range(len(action_mask)) if action_mask[i] == 1], 1)[0]
        