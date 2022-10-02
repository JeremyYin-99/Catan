# %%
import random

class Node:
    def __init__(self, id, node1=None, node2=None, node3=None, edge1=None, edge2=None, edge3=None) -> None:
        self.id = id

        self.node1 = node1
        self.node2 = node2
        self.node3 = node3

        self.edge1 = edge1
        self.edge2 = edge2
        self.edge3 = edge3

        self.occupied = False

    def getID(self):
        return self.id

    def setNode1(self, node):
        self.node1 = node

    def setNode2(self, node):
        self.node2 = node
    
    def setNode3(self, node):
        self.node3 = node

    def setOccupied(self):
        self.occupied = True

    def getOccupied(self):
        return self.occupied

    def getConnections(self):
        if (self.node3 == None):
            return (self.id, self.node1.getID(), self.node2.getID())
        else:
            return (self.id, self.node1.getID(), self.node2.getID(), self.node3.getID())

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

    def setNodes(self, node1, node2, node3, node4, node5, node6):
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.node4 = node4
        self.node5 = node5
        self.node6 = node6



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

    node_graph = {
        1:(2,9),
        2:(1,3),
        3:(2,4,11),
        4:(3,5),
        5:(4,6,13),
        6:(5,7),
        7:(6,15),
        8:(9,18),
        9:(1,8,10),
        10:(9,11,20),
        11:(3,10,12),
        12:(11,13,22),
        13:(5,12,14),
        14:(13,15,24),
        15:(7,14,16),
        16:(15,26),
        17:(18,28),
        18:(8,17,19),
        19:(18,20,30),
        20:(10,19,21),
        21:(20,22,32),
        22:(12,21,23),
        23:(22,24,34),
        24:(14,23,25),
        25:(24,26,36),
        26:(16,25,27),
        27:(26,38),
        28:(17,29),
        29:(28,30,39),
        30:(19,29,31),
        31:(30,32,41),
        32:(21,31,33),
        33:(32,34,43),
        34:(23,33,35),
        35:(34,36,45),
        36:(25,35,37),
        37:(36,38,47),
        38:(27,37),
        39:(29,40),
        40:(39,41,48),
        41:(31,40,42),
        42:(41,43,50),
        43:(33,42,44),
        44:(43,45,52),
        45:(35,44,46),
        46:(45,47,54),
        47:(37,46),
        48:(40,49),
        49:(48,50),
        50:(42,49,51),
        51:(50,52),
        52:(44,51,53),
        53:(52,54),
        54:(46,53)
    }

    tile_node_graph = {
        1:(1,2,3,9,10,11),
        2:(3,4,5,11,12,13),
        3:(5,6,7,13,14,15),
        4:(8,9,10,18,19,20),
        5:(10,11,12,20,21,22),
        6:(12,13,14,22,23,24),
        7:(14,15,16,24,25,26),
        8:(17,18,19,28,29,30),
        9:(19,20,21,30,31,32),
        10:(21,22,23,32,33,34),
        11:(23,24,25,34,35,36),
        12:(25,26,27,36,37,38),
        13:(29,30,31,39,40,41),
        14:(31,32,33,41,42,43),
        15:(33,34,35,43,44,45),
        16:(35,36,37,45,46,47),
        17:(40,41,42,48,49,50),
        18:(42,43,44,50,51,52),
        19:(44,45,46,52,53,54)
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
                        "lumber","lumber","lumber","lumber"
                        ]
        self.id = []
        self.available_id = []
        for val in range(19):
            self.id.append(val+1)
            self.available_id.append(val+1)


        self.high_values = [6,6,8,8]
        self.low_values = [3,3,4,4,5,5,9,9,10,10,11,11]
        self.very_low_values = [2,12]

        # add in 6 and 8
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

        # add in 2 and 12
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

        # add in everything else besides desert
        for low_val in self.low_values:
            random_id = random.choice(self.id)
            random_resource = random.choice(self.resource)

            # remove the random choice
            self.resource.remove(random_resource)
            self.id.remove(random_id)

            self.tile_all.append(Tile(random_id, low_val, random_resource))
        
        # add the desert
        self.tile_all.append(Tile(self.id[0],7,"desert"))

        # Work on initializing the Nodes (City/Settlement)
        # Initialize nodes
        for k in self.node_graph.keys():
            self.node_all.append(Node(k))

        # connect nodes
        for node in self.node_all:
            connections = self.node_graph[node.getID()]
            i = 0
            for element in connections:
                if i == 0:
                    node.setNode1(self.node_all[element-1])
                elif i == 1:
                    node.setNode2(self.node_all[element-1])
                elif i == 2:
                    node.setNode3(self.node_all[element-1])
                else:
                    print("Issues have happened")
                i = i+1

        # Work on initailizing the Edges (Roads)


        # Connect nodes to tiles


        # Work on initalizing the Players


        # Append instance of game to class variable
        Game.all.append(self)



# %%

