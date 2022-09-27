# %%
import random

class Node:
    def __init__(self, id, edge1, edge2, edge3=None) -> None:
        self.id = id

        self.edge1 = edge1
        self.edge2 = edge2
        self.edge3 = edge3

        self.occupied = False


    def setOccupied(self):
        self.occupied = True

    def getOccupied(self):
        return self.occupied

class Edge:
    def __init__(self) -> None:
        self.occupied = False


    def getOccupied(self):
        return self.occupied

class Tile:
    def __init__(self, id, value, resource) -> None:
        self.id = id
        self.value = value
        self.resource = resource



class Player:
    def __init__(self, name) -> None:
        self.name = name

        self.vp = 0

        self.resource = {
            "wool": 0,
            "lumber": 0,
            "grain": 0,
            "ore": 0,
            "brick": 0
        }

        self.road_building = 0
        self.year_of_plenty = 0
        self.monopoly = 0

        self.largest_army = False
        self.longest_road = False


    def addResource(self, type, amount):
        self.resource[type] = self.resource[type] + amount

    def buildRoad(self, game_check: False):
        if game_check ==False:
            print(f"A road is already built")
            return -1

        if (self.resource["brick"] >= 1) and (self.resource["lumber"] >= 1):
            self.resource["brick"] = self.resource["brick"] - 1
            self.resource["lumber"] = self.resource["lumber"] - 1
            print(f"{self.name} has built a road")
            return 1
        else:
            print(f"{self.name} does not enough resources to build a road")
            return -1

    def buildSettlement(self, game_check: False):
        if game_check == False:
            print(f"A settlement or city is already built")
            return -1
            

        if (self.resource["brick"] >= 1) and (self.resource["lumber"] >= 1) and (self.resource["wool"] >= 1) and (self.resource["grain"]):
            self.resource["brick"] = self.resource["brick"] - 1
            self.resource["lumber"] = self.resource["lumber"] - 1
            self.resource["wool"] = self.resource["wool"] - 1
            self.resource["grain"] = self.resource["grain"] - 1
            print(f"{self.name} has built a settlement")
            return 1
        else:
            print(f"{self.name} does not enough resources to build a settlement")
            return -1

    def buildCity(self, game_check: False):
        if game_check == False:
            print(f"A settlement or city is already built")
            return -1

        if (self.resource["grain"] >= 2) and (self.resource["ore"] >= 3):
            self.resource["grain"] = self.resource["grain"] - 2
            self.resource["ore"] = self.resource["ore"] - 3
            print(f"{self.name} has built a city")
            return 1
        else:
            print(f"{self.name} does not enough resources to build a city")
            return -1

    


class Game:
    # store all game instances
    all = []
    # Create graph when game is initialized
    tile_graph = {
        1:(2,4,5),
        2:(1,3,5,6),
        3:(2,6,7),
        4:(1,5,8,9),
        5:(1,2,4,6,9,10),
        6:(2,3,5,7,10,11),
        7:(3,6,11,12),
        8:(4,9,13),
        9:(4,5,8,10,13,14),
        10:(4,5,9,11,14,15),
        11:(6,7,10,12,15,16),
        12:(7,11,16),
        13:(8,9,14,17),
        14:(9,10,13,15,17,18),
        15:(10,11,14,16,18,19),
        16:(11,12,15,19),
        17:(13,14,18),
        18:(14,15,17,19),
        19:(15,16,18)
    }

    def __init__(self, player1nam="P1", player2name="P2", player3name="P3", player4name="P4") -> None:
        # place to put class instances related to this game instance
        self.tile_all = []
        self.node_all = []
        self.edge_all = []
        self.player_all = []

        # work on initializing the Tiles
        self.values = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
        self.resource = ["brick","brick","brick",
                        "ore","ore","ore",
                        "wool","wool","wool","wool",
                        "grain","grain","grain","grain",
                        "lumber","lumber","lumber","lumber",
                        "desert"]
        self.id = []
        self.available_id = []
        for val in range(19):
            self.id.append(val+1)
            self.available_id.append(val+1)


        self.high_values = [6,6,8,8]
        self.low_values = [3,3,4,4,5,5,9,9,10,10,11,11]
        self.very_low_values = [2,12]
        for high_val in self.high_values:
            # get random choice of available id
            random_id = random.choice(self.available_id)
            random_resource = random.choice(self.resource)

            # remove the random choice
            self.resource.remove(random_resource)
            self.id.remove(random_id)

            # update available id using graph
            self.available_id.remove(random_id)
            for graph_val in self.tile_graph[random_id]:
                if graph_val in self.available_id:
                    self.available_id.remove(graph_val)

            # create Tile
            self.tile_all.append(Tile(random_id, high_val, random_resource))

        self.available_id = self.id.copy()
        
        for very_low_val in self.very_low_values:
            random_id = random.choice(self.available_id)
            random_resource = random.choice(self.resource)

            # remove the random choice
            self.resource.remove(random_resource)
            self.id.remove(random_id)

            # update available id using graph
            self.available_id.remove(random_id)
            for graph_val in self.tile_graph[random_id]:
                if graph_val in self.available_id:
                    self.available_id.remove(graph_val)

            # create Tile
            self.tile_all.append(Tile(random_id, very_low_val, random_resource))


        for low_val in self.low_values:
            random_id = random.choice(self.id)
            random_resource = random.choice(self.resource)

            # remove the random choice
            self.resource.remove(random_resource)
            self.id.remove(random_id)

            self.tile_all.append(Tile(random_id, low_val, random_resource))
        
        # Work on initializing the Nodes (City/Settlement)

        # Work on initailizing the Edges (Roads)

        # Work on initalizing the Players

        # Append instance of game to class variable
        Game.all.append(self)




# %%

