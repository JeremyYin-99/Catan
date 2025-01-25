from board import *
import random
import numpy as np
from helper_dicts import resources, port_types

# Create the Action class which will contain all the actions that can be taken in the game. The actions will be defined as methods of the Action class and will take in the player, game, and action as arguments. The action space will be defined as a dictionary with the action_id as the key and the action as the value. The action_id will be a number corrosponding to a unique action. For example, if the player wants to build a settlement on node 1, the action_id will be 1.


class Action:
    # The action_id will be a number corrosponding to a unique action. For example, if the player wants to build a settlement on node 1, the action_id will be 1.

    # Initialize the action space
    def __init__(self, player_num, board: Board):
        self.player_num = player_num
        self.board = board
        self.action_id = None
        # self.action_space()
        # self.action_space = {1: self.build_settlement, 2: self.build_city, 3: self.build_road, 4: self.move_robber, 5: self.trade,
        #                      6: self.buy_development_card, 7: self.play_knight, 8: self.play_road_building, 9: self.play_year_of_plenty, 10: self.play_monopoly, 11: self.end_turn}        

    def build_settlement(self, node_num) -> bool:
        # Check if the game is in the setup phase
        if (self.board.nodes[node_num].settlement_type == 0):
            for node in self.board.nodes[node_num].node_connections:
                if self.board.nodes[node].settlement_type != 0:
                    print("The node is next to another settlement")
                    return False
                
        if self.board.setup_phase:
            # Check if 1) the node is empty, 2) the nodes adjacent to the node are empty, 3) the player has enough settlements
            # Build the settlement
            self.board.players[self.player_num].settlements_available -= 1
            self.board.players[self.player_num].victory_points += 1
            self.board.nodes[node_num].settlement_type = 1
            # add the settlement to the player's settlement_list
            self.board.players[self.player_num].settlement_list.append(
                self.board.nodes[node_num])
            return True
        
        # Check if the player has enough resources to build a settlement
        if not(self.board.players[self.player_num].resources["lumber"] >= 1 and self.board.players[self.player_num].resources["brick"] >= 1 and self.board.players[self.player_num].resources["sheep"] >= 1 and self.board.players[self.player_num].resources["grain"] >= 1):
            print("The player does not have enough resources to build a settlement.")
            return False
        
        # Check if the player has enough settlements to build a settlement
        if self.board.players[self.player_num].settlements < 1:
            print("The player does not have enough settlements to build a settlement.")
            return False
        
        # Check if the node is empty for both settlement and city
        if self.board.nodes[node_num].settlement_type != 0:
            if self.board.nodes[node_num].settlement_type == 1:
                print("The node is already a settlement")
            else:
                print("The node is already a city")
            return False
        
        # Check if the node is connected to a road owned by the player
        connected_road = False
        for edge in self.board.nodes[node_num].edges:
            if self.board.edges[edge].owner == self.player_num:
                # Build the settlement
                connected_road = True
        
        if not connected_road:
            print("The node is not connected to a road owned by the player.")
            return False

        # update player information
        self.board.players[self.player_num].settlements -= 1
        self.board.players[self.player_num].victory_points += 1
        # add the settlement to the player's settlement_list
        self.board.players[self.player_num].settlement_list.append(
            node_num)
        
        # update node information
        self.board.nodes[node_num].owner = self.player_num
        self.board.nodes[node_num].settlement_type = 1

        # Take away the resources
        self.board.players[self.player_num].resources["lumber"] -= 1
        self.board.players[self.player_num].resources["brick"] -= 1
        self.board.players[self.player_num].resources["wool"] -= 1
        self.board.players[self.player_num].resources["grain"] -= 1
        return True
  
    # Define build_city
    def build_city(self, node_num) -> bool:
        # Check if the player owns the node
        if self.board.nodes[node_num].owner != self.player_num:
            print("The player does not own the node.")
            return False
        
        # Check if the player has enough resources to build a city
        if not(self.board.players[self.player_num].resources["grain"] >= 2 and self.board.players[self.player_num].resources["ore"] >= 3):
            print("The player does not have enough resources to build a city.")
            return False
        
        # Check if the player has enough cities to build a city
        if self.board.players[self.player_num].cities < 1:
            print("The player does not have enough cities to build a city.")
            return False
        
        # Check if the node has a settlement owned by the player
        if self.board.nodes[node_num].settlement_type != 1:
            print("The node does not have a settlement owned by the player.")
            return False
        
        # Build the city
        # update player information
        self.board.players[self.player_num].cities -= 1
        self.board.players[self.player_num].victory_points += 1
        # update node information
        self.board.nodes[node_num].settlement_type = 2

        # Take away the resources
        self.board.players[self.player_num].resources["grain"] -= 2
        self.board.players[self.player_num].resources["ore"] -= 3

        return True
    
    def build_road(self, edge_num) -> bool:
        # Check if the game is in the setup phase
        # Check if the edge is empty
        if self.board.edges[edge_num].owner is not None:
            print("The edge is not empty.")
            return False
        
        # Check if the edge is connected to a node owned by the player
        connected_node = False
        for node in self.board.edges[edge_num].nodes:
            if (self.board.nodes[node].settlement_type != 0) and (self.board.nodes[node].owner == self.player_num):
                connected_node = True
        if not connected_node:
            print("The edge is not connected to a node owned by the player.")
            return False
        
        if self.board.setup_phase:
            # Build the road for free during setup phase
            self.board.edges[edge_num].owner = self.player_num
            self.board.players[self.player_num].roads -= 1
            return True
        
        # Check if the player has enough resources to build a road
        if not(self.board.players[self.player_num].resources["lumber"] >= 1 and self.board.players[self.player_num].resources["brick"] >= 1):
            print("The player does not have enough resources to build a road.")
            return False
        
        # Check if the player has enough roads to build a road
        if self.board.players[self.player_num].roads < 1:
            print("The player does not have enough roads to build a road.")
            return False
        
        # Build the road
        # update the board
        self.board.edges[edge_num].road = self.player_num
        # update the player
        self.board.players[self.player_num].roads -= 1
        # remove resources
        self.board.players[self.player_num].resources["lumber"] -= 1
        self.board.players[self.player_num].resources["brick"] -= 1
        return True

    # Define move_robber
    def move_robber(self, tile_number) -> bool:
        # Check if the target tile is not the current tile
        if self.board.robber_tile == tile_number:
            print("The robber is already on the target tile.")
            return False
        
        # Move the robber
        self.board.tiles[self.board.robber_tile].robber = False
        self.board.tiles[tile_number].robber = True
        self.board.robber_tile = tile_number
        
        # rob a random player (not self) on the target tile
        players_on_tile = []
        for node in self.board.tiles[tile_number].nodes:
            if self.board.nodes[node].settlement_type != 0:
                players_on_tile.append(self.board.nodes[node].owner)
        players_on_tile = list(set(players_on_tile))

        if len(players_on_tile) > 0:
            player_to_rob = random.choice(players_on_tile)
            # take a random resource from the player
            resources = list(self.board.players[player_to_rob].resources.keys())
            resource = random.choice(resources)
            self.board.players[self.player_num].resources[resource] += 1
            self.board.players[player_to_rob].resources[resource] -= 1
        return True
        

    # Define trade with the bank
    def trade(self, trade_type, trade_resources, trade_amount) -> bool:
        # Check if the player has access to the trade
        pass

    # Define player accept trade

    # Define player reject trade

    # Define buy_development_card
    def buy_development_card(self) -> bool:
        # Check if the player has enough resources to buy a development card
        if not(self.board.players[self.player_num].resources["grain"] >= 1 and self.player.resources["sheep"] >= 1 and self.board.players[self.player_num].resources["ore"] >= 1):
            print("The player does not have enough resources to buy a development card.")
            return False
        
        # Check if there are development cards left
        if len(self.board.development_cards) < 1:
            print("There are no development cards left.")
            return False
        
        # Take away the resources
        self.board.players[self.player_num].resources["grain"] -= 1
        self.board.players[self.player_num].resources["sheep"] -= 1
        self.board.players[self.player_num].resources["ore"] -= 1
        # Take away the development card from the game
        card = random.choice(self.board.development_cards)
        self.board.development_cards.remove(card)

        # Set can_play_development_card to False
        self.board.players[self.player_num].can_play_development_card = False

        # Add the development card to the player's hand
        self.board.players[self.player_num].development_cards[card] += 1
        return True

    # Define play_knight
    def play_knight(self, target_tile, player_num) -> bool:
        # Check if the player can play development cards
        if self.board.players[self.player_num].can_play_development_card == False:
            print("The player cannot play development cards.")
            return False
        
        # Check if the player has a knight card
        if self.board.players[self.player_num].development_cards["knight"] < 1:
            print("The player does not have a knight card.")
            return False
        
        # Check if the player has not played a knight card this turn
        if self.board.players[self.player_num].knight_this_turn:
            print("The player has already played a knight card this turn.")
            return False
        
        # Play the knight card
        rob = self.move_robber(target_tile)
        if not rob:
            print("The robber could not be moved.")
            return False
        
        # Take away the knight card
        self.board.players[self.player_num].development_cards["knight"] -= 1
        # Add the knight card to the player's played knights
        self.board.players[self.player_num].played_knights += 1
        
        return True        
            

    # Define play_year_of_plenty
    def play_year_of_plenty(self, resource1, resource2) -> bool:
        # Check if the player can play development cards
        if self.board.players[self.player_num].can_play_development_card == False:
            print("The player cannot play development cards.")
            return False
        # Check if the player has a year of plenty card
        if self.board.players[self.player_num].development_cards["year_of_plenty"] > 0:
            # Play the year of plenty card
            # Take away the year of plenty card
            self.board.players[self.player_num].development_cards["year_of_plenty"] -= 1
            # Add the resources to the player's resources
            self.board.players[self.player_num].resources[resource1] += 1
            self.board.players[self.player_num].resources[resource2] += 1
            # Change the players development card usage
            self.board.players[self.player_num].can_play_development_card = False
            return True
        print("The player does not have a year of plenty card.")
        return False

    # Define play_road_building
    def play_road_building(self) -> bool:
        # Check if the player can play development cards
        if self.board.players[self.player_num].can_play_development_card == False:
            print("The player cannot play development cards.")
            return False
        # Check if the player has a road building card
        if self.board.players[self.player_num].development_cards["road_building"] > 0:
            # Play the road building card
            # Take away the road building card
            self.board.players[self.player_num].development_cards["road_building"] -= 1
            # Add two roads to the player's roads
            self.board.players[self.player_num].to_build = 2
            # Change the players development card usage
            self.board.players[self.player_num].can_play_development_card = False
            return True
        print("The player does not have a road building card.")
        return False

    # Define play_monopoly

    def play_monopoly(self, resource) -> bool:
        # Check if the player can play development cards
        if self.board.players[self.player_num].can_play_development_card == False:
            print("The player cannot play development cards.")
            return False
        # Check if the player has a monopoly card
        if self.board.players[self.player_num].development_cards["monopoly"] > 0:
            # Play the monopoly card
            # Take away the monopoly card
            self.board.players[self.player_num].development_cards["monopoly"] -= 1
            # Take away the resources from the other players
            for player in self.board.players:
                if player.player_num != self.player_num:
                    self.board.players[self.player_num].resources[resource] += player.resources[resource]
                    player.resources[resource] = 0
            # Change the players development card usage
            self.board.players[self.player_num].can_play_development_card = False
            return True
        print("The player does not have a monopoly card.")
        return False

    # Define end_turn
    def end_turn(self) -> bool:
        # Reallow the player to play development cards
        self.board.players[self.player_num].can_play_development_card = True
        self.board.players[self.player_num].has_rolled = False
        return True

    # Define discard_cards
    def discard_cards(self, resource):
        if self.board.players[self.player_num].to_discard > 0:
            # check if the player has the resource
            if self.board.players[self.player_num].resources[resource] > 0:
                # remove the resource from the player's resources
                self.board.players[self.player_num].resources[resource] -= 1
                self.board.players[self.player_num].to_discard -= 1
                return True
        return False

    # roll_dice
    def roll_dice(self):
        self.board.dice_roll = random.randint(1, 6) + random.randint(1, 6)
        self.board.players[self.player_num].has_rolled = True
        # check if a 7 was rolled
        if self.board.dice_roll == 7:
            for player in self.board.players:
                if sum(player.resources.values()) > 7:
                    player.to_discard = round(sum(player.resources.values())/2)
                    player.discard = True

    # # define the action mask

    # def get_action_mask(self):
    #     # check which moves are legal for the current player
    #     # if the game is in the setup phase, the player can only build settlements and roads
    #     # if the dice has not been rolled, the player can also roll the dice
    #     # filter order: check if it is the setup phase, check if the dice has been rolled, check resources constraints, check development cards on hand, check for ports, check for trade options.
    #     # Finally return the action mask
    #     mask = []

    #     # check settlements
    #     # check setup phase
    #     if self.board.setup_phase:
    #         for node in self.board.nodes.values():
    #             if node.settlement_type == 0:
    #                 mask.append(True)
    #             else:
    #                 mask.append(False)
    #     # check if the player has enough resources
    #     elif self.board.players[self.player_num].resources["lumber"] >= 1 and self.board.players[self.player_num].resources["brick"] >= 1 and self.board.players[self.player_num].resources["sheep"] >= 1 and self.board.players[self.player_num].resources["grain"] >= 1:
    #         for node in self.board.nodes.values():
    #             if node.settlement_type == 0:
    #                 mask.append(True)
    #             else:
    #                 mask.append(False)
    #     else:
    #         for node in self.board.nodes.values():
    #             mask.append(False)

    #     # check roads
    #     # check setup phase
    #     if self.board.setup_phase:
    #         for edge in self.board.edges.values():
    #             check = False
    #             for node_num in edge.nodes:
    #                 node = self.board.nodes[node_num]
    #                 if node.settlement_type == 0 and node.owner == self.player_num:
    #                     if edge.road == None:
    #                         check = True
    #                     else:
    #                         pass
    #             mask.append(check)
    #     # check if the player has enough resources
    #     elif self.board.players[self.player_num].resources["lumber"] >= 1 and self.board.players[self.player_num].resources["brick"] >= 1:
    #         for edge in self.board.edges.values():
    #             if edge.road == None:
    #                 mask.append(True)
    #             else:
    #                 mask.append(False)
    #     else:
    #         for edge in self.board.edges.values():
    #             mask.append(False)

    #     # check cities
    #     # check if the player has enough resources
    #     if self.board.players[self.player_num].resources["grain"] >= 2 and self.board.players[self.player_num].resources["ore"] >= 3:
    #         for node in self.board.nodes.values():
    #             if node.settlement_type == 1 and node.settlement.player_num == self.player_num:
    #                 mask.append(True)
    #             else:
    #                 mask.append(False)
    #     else:
    #         for node in self.board.nodes.values():
    #             mask.append(False)

    #     # check development cards
    #     # check if the player has enough resources
    #     if self.board.players[self.player_num].resources["grain"] >= 1 and self.board.players[self.player_num].resources["sheep"] >= 1 and self.board.players[self.player_num].resources["ore"] >= 1:
    #         mask.append(True)
    #     else:
    #         mask.append(False)

    #     # check robber
    #     for i in self.board.tiles:
    #         for j in range(len(self.board.players)):
    #             if j != self.player_num:
    #                 mask.append(False)

    #     # check knight
    #     # check if player can has a knight card and can play dev card
    #     if self.board.players[self.player_num].dev_cards["knight"] > 0 and self.board.players[self.player_num].can_play_dev_card:
    #         for i in self.board.tiles:
    #             for j in self.board.players:
    #                 check = False
    #                 if j.player_num != self.player_num:
    #                     # check if player is on the tile
    #                     for node in self.board.tiles[i].nodes:
    #                         if node.settlement != None and node.settlement.player_num == j.player_num:
    #                             check = True
    #                         elif node.city != None and node.city.player_num == j.player_num:
    #                             check = True
    #                         else:
    #                             pass
    #                     mask.append(check)
    #     else:
    #         for i in self.board.tiles:
    #             for j in self.board.players:
    #                 if j.player_num != self.player_num:
    #                     mask.append(False)

    #     # check year of plenty
    #     # check if player can has a year of plenty card and can play dev card
    #     if self.board.players[self.player_num].dev_cards["year_of_plenty"] > 0 and self.board.players[self.player_num].can_play_dev_card:
    #         for i in range(5):
    #             mask.append(True)
    #     else:
    #         for i in range(5):
    #             mask.append(False)

    #     # road building
    #     # check if player can has a road building card and can play dev card
    #     if self.board.players[self.player_num].dev_cards["road_building"] > 0 and self.board.players[self.player_num].can_play_dev_card:
    #         mask.append(True)
    #     else:
    #         mask.append(False)

    #     # monopoly
    #     # check if player can has a monopoly card and can play dev card
    #     if self.board.players[self.player_num].dev_cards["monopoly"] > 0 and self.board.players[self.player_num].can_play_dev_card:
    #         for i in range(5):
    #             mask.append(True)
    #     else:
    #         for i in range(5):
    #             mask.append(False)

    #     # end turn
    #     # check if the dice have been rolled
    #     if self.board.players[self.player_num].has_rolled:
    #         mask.append(True)
    #     else:
    #         mask.append(False)

    #     return mask

    #     pass

    # def get_robber_action_mask(self):
    #     pass

    # def get_discard_action_mask(self):
    #     pass

    # def get_road_set_up_mask(self):
    #     mask = []

    #     # check settlements
    #     # check setup phase
    #     for node in self.board.nodes.values():
    #         mask.append(False)

    #     # check roads
    #     # check setup phase
    #     if self.board.setup_phase:
    #         for edge in self.board.edges.values():
    #             check = False
    #             for node_num in edge.nodes:
    #                 node = self.board.nodes[node_num]
    #                 if node.settlement == self.player_num:
    #                     if edge.road == None:
    #                         check = True
    #                     else:
    #                         pass
    #             mask.append(check)
    #     # check if the player has enough resources
    #     elif self.board.players[self.player_num].resources["lumber"] >= 1 and self.board.players[self.player_num].resources["brick"] >= 1:
    #         for edge in self.board.edges.values():
    #             if edge.road == None:
    #                 mask.append(True)
    #             else:
    #                 mask.append(False)
    #     else:
    #         print("not enough resources")
    #         for edge in self.board.edges.values():
    #             mask.append(False)

    #     # check cities
    #     # check if the player has enough resources
    #     for node in self.board.nodes.values():
    #         mask.append(False)

    #     # check development cards
    #     # check if the player has enough resources
    #     mask.append(False)

    #     # check robber
    #     for i in self.board.tiles:
    #         for j in range(len(self.board.players)):
    #             if j != self.player_num:
    #                 mask.append(False)

    #     # check knight
    #     # check if player can has a knight card and can play dev card
    #     for i in self.board.tiles:
    #         for j in self.board.players:
    #             if j.player_num != self.player_num:
    #                 mask.append(False)

    #     # check year of plenty
    #     # check if player can has a year of plenty card and can play dev card
    #     for i in range(5):
    #         mask.append(False)

    #     # road building
    #     # check if player can has a road building card and can play dev card
    #     mask.append(False)

    #     # monopoly
    #     # check if player can has a monopoly card and can play dev card
    #     for i in range(5):
    #         mask.append(False)

    #     # end turn
    #     # check if the dice have been rolled
    #     mask.append(False)

    #     return mask

    # def get_settlement_set_up_mask(self):
    #     mask = []

    #     # check settlements
    #     # check setup phase
    #     if self.board.setup_phase:
    #         for node in self.board.nodes.values():
    #             if node.settlement_type == 0:
    #                 mask.append(True)
    #             else:
    #                 mask.append(False)
    #     # check if the player has enough resources
    #     elif self.board.players[self.player_num].resources["lumber"] >= 1 and self.board.players[self.player_num].resources["brick"] >= 1 and self.board.players[self.player_num].resources["sheep"] >= 1 and self.board.players[self.player_num].resources["grain"] >= 1:
    #         for node in self.board.nodes.values():
    #             if node.settlement == None and node.city == None:
    #                 mask.append(True)
    #             else:
    #                 mask.append(False)
    #     else:
    #         for node in self.board.nodes.values():
    #             mask.append(False)

    #     # check roads
    #     # check setup phase
    #     # check if the player has enough resources
    #     for edge in self.board.edges.values():
    #         mask.append(False)

    #     # check cities
    #     # check if the player has enough resources
    #     for node in self.board.nodes.values():
    #         mask.append(False)

    #     # check development cards
    #     # check if the player has enough resources
    #     mask.append(False)

    #     # check robber
    #     for i in self.board.tiles:
    #         for j in range(len(self.board.players)):
    #             if j != self.player_num:
    #                 mask.append(False)

    #     # check knight
    #     # check if player can has a knight card and can play dev card
    #     for i in self.board.tiles:
    #         for j in self.board.players:
    #             if j.player_num != self.player_num:
    #                 mask.append(False)

    #     # check year of plenty
    #     # check if player can has a year of plenty card and can play dev card
    #     for i in range(5):
    #         mask.append(False)

    #     # road building
    #     # check if player can has a road building card and can play dev card
    #     mask.append(False)

    #     # monopoly
    #     # check if player can has a monopoly card and can play dev card
    #     for i in range(5):
    #         mask.append(False)

    #     # end turn
    #     # check if the dice have been rolled
    #     mask.append(False)

    #     return mask

    # def get_road_building_action_mask(self):
    #     pass

    # # Define the action space
    # def action_space(self):
    #     self.action_list = {}
    #     val = 0

    #     # Add actions for settlements
    #     for i in self.board.nodes:
    #         self.action_list[val] = [self.build_settlement, [i]]
    #         val += 1

    #     # Add actions for roads
    #     for i in self.board.edges:
    #         self.action_list[val] = [self.build_road, [i]]
    #         val += 1

    #     # Add actions for cities
    #     for i in self.board.nodes:
    #         self.action_list[val] = [self.build_city, [i]]
    #         val += 1

    #     # Add actions for development cards
    #     self.action_list[val] = [self.buy_development_card, []]
    #     val += 1

    #     # Add actions for robber
    #     for i in self.board.tiles:
    #         for j in range(len(self.board.players)):
    #             if j != self.player_num:
    #                 self.action_list[val] = [self.move_robber, [i, j]]
    #                 val += 1

    #     # Add actions for knight
    #     for i in self.board.tiles.values():
    #         for j in self.board.players:
    #             if j.player_num != self.player_num:
    #                 self.action_list[val] = [
    #                     self.play_knight, [i, j.player_num]]
    #                 val += 1

    #     # Add actions for year of plenty
    #     for i in resource_str_to_num:
    #         for j in resource_str_to_num:
    #             self.action_list[val] = [self.play_year_of_plenty, [i, j]]
    #             val += 1

    #     # Add actions for road building
    #     self.action_list[val] = [self.play_road_building, []]
    #     val += 1

    #     # Add actions for monopoly
    #     for i in resource_str_to_num:
    #         self.action_list[val] = [self.play_monopoly, [i]]
    #         val += 1

    #     # Add actions for end turn
    #     self.action_list[val] = [self.end_turn, []]
    #     val += 1

    #     return self.action_list

    # # Define make_move which plays the move specified by the player using the action_id

    def make_move(self, action_id) -> bool:
        mask = self.get_action_mask()
        if mask[action_id] == 0 or mask[action_id] is False:
            return False

        # check if the dice was rolled #### FIX THIS
        if self.action_list[action_id][0] == self.roll_dice:
            return self.action_list[action_id][0](), "Discard cards"

        # check if action is end turn
        if self.action_list[action_id][0] == self.end_turn:
            return self.action_list[action_id][0](), "End turn"

        # check if action is road building
        if self.action_list[action_id][0] == self.play_road_building:
            return self.action_list[action_id][0](), "Road building"

        # make the move
        if self.action_list[action_id][1] == []:
            return self.action_list[action_id][0](), "Move made"
        elif len(self.action_list[action_id][1]) == 1:
            return self.action_list[action_id][0](self.action_list[action_id][1][0]), "Move made"
        elif len(self.action_list[action_id][1]) == 2:
            return self.action_list[action_id][0](self.action_list[action_id][1][0], self.action_list[action_id][1][1]), "Move made"
        else:
            return False
    
    ############################

    def get_settlement_mask(self):
        action_mask = []
        # 1) Check if settlements can be built on each node
        for node in node_graph:
            current_node = self.board.nodes[node]
            disqualified = False
            # 1.a) no existing settlements exist on node
            if current_node.settlement_type != 0:
                # disqualified = True
                action_mask.append(False)
                continue

            # 1.b) no existing settlements exist on adjcent tile
            for connection in current_node.node_connections:
                if self.board.nodes[connection].settlement_type != 0:
                    disqualified = True

            if disqualified == True:
                action_mask.append(False)
                continue

            if self.board.setup_phase == True:
                action_mask.append(True)
                continue
            
            # 1.c) check if player has enough settlements available
            if self.board.players[self.player_num].settlements_available <= 0:
                disqualified = True

            # 1.d) resource constraints 
            if ((self.board.players[self.player_num].resources["brick"] < 1) or 
                (self.board.players[self.player_num].resources["wool"] < 1) or 
                (self.board.players[self.player_num].resources["wheat"] < 1) or
                (self.board.players[self.player_num].resources["lumber"] < 1)
                ):
                disqualified = True

            action_mask.append(not disqualified)
            
        return np.array(action_mask)
    
    def get_city_mask(self):
        action_mask = []
        # 2) Check if city can be built
        for node in node_graph:
            current_node = self.board.nodes[node]

            # 2.a) check if player owns existing settlement on the node
            if (current_node.owner != self.player_num) or (current_node.settlement_type != 1):
                action_mask.append(False)
                continue

            # 2.b) check if player has enough resources
            if ((self.board.players[self.player_num].resources["grain"] < 2) or
                (self.board.players[self.player_num].resources["ore"] < 3)):
                action_mask.append(False)
                continue

            # 2.c) check if player has enough cities available
            if self.board.players[self.player_num].cities_available < 1:
                action_mask.append(False)
                continue

            action_mask.append(True)
        
        return np.array(action_mask)
    
    def get_road_mask(self):
        action_mask = []
        # 3) check if road can be built
        for edge in edge_graph:
            current_edge = self.board.edges[edge]

            # 3.a) edge is not currently built
            if current_edge.owner != None:
                action_mask.append(False)
                continue
            
            # 3.b) check if player owns:
                # 3.b.1) existing road adjcent to edge
                # 3.b.2) existing settlement or city connected to edge
            disqualified = True
            for connection in current_edge.edges:
                if self.board.edges[connection].owner == self.player_num:
                    disqualified = False
            
            for connection in current_edge.nodes:
                if self.board.nodes[connection].owner == self.player_num:
                    disqualified = False
            
            if disqualified:
                action_mask.append(False)
                continue

            # 3.a.0) check if road building was used and allow 2 roads
            if self.board.players[self.player_num].road_building > 0:
                action_mask.append(True)
                continue

            # 3.c.1) it is not currently the setup period
            if self.board.setup_phase:
                if len(self.board.players[self.player_num].road_list) < self.board.players[self.player_num].settlement_list:
                    action_mask.append(True)            
            elif ((self.board.players[self.player_num].resources["lumber"] > 0) and
                (self.board.players[self.player_num].resources["brick"] > 0)):
                action_mask.append(True)
            else:
                action_mask.append(False)
            
        return np.array(action_mask)

    def get_dev_card_mask(self):
        action_mask = []

        # 4) check if dev card can be purchased
            # 4.a) check if player has enough resources
        
        if ((self.board.players[self.player_num].resources["grain"] > 0) and
            (self.board.players[self.player_num].resources["wool"] > 0) and
            (self.board.players[self.player_num].resources["ore"] > 0)):
            action_mask.append(True)

        else:
            action_mask.append(False)
        
        return np.array(action_mask)
    
    def get_bank_trade_mask(self):
        action_mask = []

        for resource in resources:
            if self.board.players[self.player_num].resources[resource] > 4:
                for i in range(len(resources) - 1):
                    action_mask.append(True)
            else:
                for i in range(len(resources) - 1):
                    action_mask.append(False)

        return np.array(action_mask)

    def get_port_trade_mask(self):
        action_mask = []

        # 6.a) check if player owns the required port
        for port in set(port_types):
            has_port = False
            for node in self.board.players[self.player_num].settlement_list:
                if self.board.nodes[node].port == port:
                    has_port = True
                    continue

            # check if player has the resources
            if (has_port) and (port != "any") and (self.board.players[self.player_num].resources[port] >= 2):
                for resource in range(len(resources)-1):
                    action_mask.append(True)
            elif (has_port) and (port == "any") and (self.board.players[self.player_num].resources[port] >= 3):
                for resource in range(len(resources)-1):
                    action_mask.append(True)
            else:
                for resource in range(len(resources)-1):
                    action_mask.append(False)

        
        return np.array(action_mask)
    
    def get_knight_mask(self):
        action_mask = []

        # 7) check if player can use the knight dev card
        for tile in self.board.tiles:
            for player in self.board.players:
                disqualified = False
                # 7.a) check if player has recieved a knight this turn
                if not player.can_play_development_card == True:
                    disqualified = True
                
                # 7.b) check if player owns a knight dev card
                if player.dev_cards["knight"] < 1:
                    disqualified = True
                
                # 7.c) check if target tile is already occupied
                if player.player_num == self.player_num:
                    disqualified = True

                action_mask.append(not disqualified)
        
        return np.array(action_mask)
    
    def get_road_building_mask(self):
        action_mask = []

        # 8) check if player can use road building dev card
        # 8.a) check if player recieved road building on this turn
        # 8.b) check if player owns road building dev
        if (self.board.players[self.player_num].can_play_development_card == True) and (self.board.players[self.player_num].dev_cards["road_building"] > 0):
            action_mask.append(True)
        else:
            action_mask.append(False)
                
        
        return np.array(action_mask)
    
    def get_year_of_plenty_mask(self):
        action_mask = []

        # 9) check if player can use year of plenty dev card
        # 9.a) check if player recieved year of plenty this turn
        # 9.b) check if player owns year of plenty
        if (self.board.players[self.player_num].can_play_development_card == True) and (self.board.players[self.player_num].dev_cards["year_of_plenty"] > 0):
            for resource1 in range(len(resources)):
                for resource2 in range(len(resources)):
                    action_mask.append(True)
        else:
            for resource1 in range(len(resources)):
                for resource2 in range(len(resources)):
                    action_mask.append(False)
        
        return np.array(action_mask)
    
    def get_monopoly_mask(self):
        action_mask = []

        # 10) check if player can use monopoly dev card
        # 10.a) check if player recieved monopoly dec card this turn
        # 10.b) check if player owns monopoly dev card
        if (self.board.players[self.player_num].can_play_development_card == True) and (self.board.players[self.player_num].dev_cards["monopoly"] > 0):
            for resource in range(len(resources)):
                action_mask.append(True)
        else:
            for resource in range(len(resources)):
                action_mask.append(False)
        
        return np.array(action_mask)
    
    def get_end_turn_mask(self):
        action_mask = []

        # 11) end turn
        # check if the dice have been rolled
        if self.board.players[self.player_num].has_rolled:
            action_mask.append(True)
        else:
            action_mask.append(False)
        
        return np.array(action_mask)
    
    def get_discard_mask(self):
        action_mask = []

        # 12) discard cards
        # 12.a) check if 7 has been rolled
        # 12.b) check if player owns greater than 7 cards
        if self.board.dice_roll == 7:
            if sum(self.board.players[self.player_num].resources.values()) > 7:
                action_mask.append(True)
            else:
                action_mask.append(False)
        else:
            action_mask.append(False)
        
        return np.array(action_mask)
    
    def get_action_mask(self):
        """
        1) Check if settlements can be built on each node
            1.a) no existing settlements exist on node
            1.b) no existing settlements exist on adjcent tile
            1.c) check if player has enough settlements available
            1.d) resource constraints 
                1.d.1) it is not currently the setup period
            
        2) Check if city can be built
            2.a) check if player owns existing settlement on the node
            2.b) check if player has enough resources
            2.c) check if player has enough cities available

        3) check if road can be built
            3.a) edge is not currently built
            3.b) check if player owns:
                3.b.1) existing road adjcent to edge OR
                3.b.2) existing settlement or city connected to edge
            3.a.0) check if road building was used and allow 2 roads
            3.c) player has enough resources
                3.c.1) it is not currently the setup period

        4) check if dev card can be purchased
            4.a) check if player has enough resources

        5) check if player can trade with the bank
            5.a) check if player owns enough resources for the trades

        6) check if player can trade with the port
            6.a) check if player owns the required port
            6.b) check if player owns enough resources for the trades

        7) check if player can use the knight dev card
            7.a) check if player has recieved a knight this turn
            7.b) check if player owns a knight dev card
            7.c) check if target tile is already occupied
        
        8) check if player can use road building dev card
            8.a) check if player recieved road building on this turn
            8.b) check if player owns road building dev

        9) check if player can use year of plenty dev card
            9.a) check if player recieved year of plenty this turn
            9.b) check if player owns year of plenty

        10) check if player can use monopoly dev card
            10.a) check if player recieved monopoly dec card this turn
            10.b) check if player owns monopoly dev card

        11) end turn

        12) discard cards
            12.a) check if 7 has been rolled
            12.b) check if player owns greater than 7 cards
        """

        action_mask = np.concatenate((self.get_settlement_mask(),
                                      self.get_city_mask(),
                                      self.get_road_mask(),
                                      self.get_dev_card_mask(),
                                      self.get_bank_trade_mask(),
                                      self.get_port_trade_mask(),
                                      self.get_knight_mask(),
                                      self.get_road_building_mask(),
                                      self.get_year_of_plenty_mask(),
                                      self.get_monopoly_mask(),
                                      self.get_end_turn_mask(),
                                      self.get_discard_mask()
                                      ))


        

        return action_mask
