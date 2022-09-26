# %%
import random

class Node:
    all = []
    def __init__(self, id, edge1, edge2, edge3=None) -> None:
        self.id = id

        self.edge1 = edge1
        self.edge2 = edge2
        self.edge3 = edge3

        self.occupied = False

        Node.all.append(self)

    def setOccupied(self):
        self.occupied = True

    def getOccupied(self):
        return self.occupied

class Edge:
    all = []
    def __init__(self) -> None:
        self.occupied = False

        Edge.all.append(self)

    def getOccupied(self):
        return self.occupied

class Tile:
    all = []
    def __init__(self, id, value, resource) -> None:
        self.id = id
        self.value = value
        self.resource = resource

        Tile.all.append(self)


class Player:
    all = []
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

        Player.all.append(self)

    def addResource(self, type, amount):
        self.resource[type] = self.resource[type] + amount

    def buildRoad(self):
        if (self.resource["brick"] >= 1) and (self.resource["lumber"] >= 1):
            self.resource["brick"] = self.resource["brick"] - 1
            self.resource["lumber"] = self.resource["lumber"] - 1
            return 1
        else:
            print("Not enough resources to build road")
            return -1

    def buildSettlement(self):
        if (self.resource["brick"] >= 1) and (self.resource["lumber"] >= 1) and (self.resource["wool"] >= 1) and (self.resource["grain"]):
            self.resource["brick"] = self.resource["brick"] - 1
            self.resource["lumber"] = self.resource["lumber"] - 1
            self.resource["wool"] = self.resource["wool"] - 1
            self.resource["grain"] = self.resource["grain"] - 1
            return 1
        else:
            print("Not enough resources to build settlement")
            return -1

    def buildCity(self):
        if (self.resource["grain"] >= 2) and (self.resource["ore"] >= 3):
            self.resource["grain"] = self.resource["grain"] - 2
            self.resource["ore"] = self.resource["ore"] - 3
            return 1
        else:
            print("Not enough resources to build city")
            return -1

    


class Game:
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

    def __init__(self, seed, player1nam="P1", player2name="P2", player3name="P3", player4name="P4") -> None:
        self.seed = seed
        self.values = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
        self.id = []
        for val in range(19):
            self.id.append(val+1)

        # shuffle values and ids
        self.shuffled_values = self.values.copy()
        random.shuffle(self.shuffled_values, self.returnSeed)

        self.shuffled_id = self.id.copy()
        random.shuffle(self.shuffled_id, self.returnSeed)
        # Instantiate tiles
        for i in range(self.shuffled_id):
            Tile(self.shuffled_id,self.shuffled_values)

    def returnSeed(self):
        return self.seed



# %%
