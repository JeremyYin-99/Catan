# %%
import random
from numpy.random import randint

resource_num_to_str = {
    1:"wool",
    2:"lumber",
    3:"grain",
    4:"ore",
    5:"brick",
    -1:"desert",
    6:"3-1"
}

resource_str_to_num = {
    "wool":1,
    "lumber":2,
    "grain":3,
    "ore":4,
    "brick":5,
    "desert":-1,
    "3-1":6

}

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
        self.settlement_type = ""
        self.player = None

        self.port = None
        self.port_num = 0
        

    def getConnections(self):
        if (self.node3 == None):
            return (self.id, self.node1.getID(), self.node2.getID())
        else:
            return (self.id, self.node1.getID(), self.node2.getID(), self.node3.getID())

    def occupyNode(self, player):
        if self.player.id != player.id:
            print('Node already settled on')
            return False

        if self.settlement_type == "":
            self.occupied = True
            self.player = player
            self.settlement_type = "Settlement"
            return True
        elif self.settlement_type == "City":
            print("City has already been built")
            return False
        elif self.settlement_type == "Settlement":
            print("Settlement has already been built")
            return False

        print("Something Unexpected happened")
        return False

    def upgradeNode(self, player):
        if self.player.id != player.id:
            print('Node already settled on')
            return False

        if self.settlement_type == "Settlement":
            self.settlement_type = "City"
            return True
        elif self.settlement_type == "":
            print("build a settlement first")
            return False
        else:
            print("A city has been built here already")
            return False


    def assignPort(self, port_type):
        self.port_num = port_type
        if port_type >=1 and port_type <=6:
            self.port = resource_num_to_str[port_type]
        else:
            print("Problem assigning port with type {}".format(port_type))
            self.port_num = 0
            return False
        return True

    def nodeState(self):
        to_return = []
        # discretize occupied structure
        if self.settlement_type == "":
            to_return.append(0)
        elif self.settlement_type == "Settlement":
            to_return.append(1)
        elif self.settlement_type == "City":
            to_return.append(2)
        else:
            print("issue stating settlement type")
            return False

        # discretize player status
        if self.player == None:
            to_return.append(0)
        else:
            to_return.append(self.player.id)

        #Discretize port state
        to_return.append(self.port_num)

        return to_return

    def __str__(self) -> str:
        if self.node3 == None:
            if self.player == None:
                to_return = 'ID: ' + str(self.id) + "\n" \
                        + "Node 1 ID: " + str(self.node1.id) + " " + "Edge 1 ID: " + str(self.edge1.id) + "\n" \
                        + "Node 2 ID: " + str(self.node2.id) + " " + "Edge 2 ID: " + str(self.edge2.id) +"\n" \
                        + "Port: " + str(self.port) + "\n" \
                        + 'Node occupation is: ' + str(self.occupied)
            else:
                to_return = 'ID: ' + str(self.id) + "\n" \
                            + "Node 1 ID: " + str(self.node1.id) + " " + "Edge 1 ID: " + str(self.edge1.id) + "\n" \
                            + "Node 2 ID: " + str(self.node2.id) + " " + "Edge 2 ID: " + str(self.edge2.id) +"\n" \
                            + "Port: " + str(self.port) + "\n" \
                            + 'Node occupation is: ' + str(self.occupied) \
                            + " by " + str(self.player.disp_name)
        else:
            if self.player== None:
                to_return = 'ID: ' + str(self.id) + "\n" \
                        + "Node 1 ID: " + str(self.node1.id) + " " + "Edge 1 ID: " + str(self.edge1.id) + "\n" \
                        + "Node 2 ID: " + str(self.node2.id) + " " + "Edge 2 ID: " + str(self.edge2.id) +"\n" \
                        + "Node 3 ID: " + str(self.node3.id) + " " + "Edge 3 ID: " + str(self.edge3.id) +"\n" \
                        + "Port: " + str(self.port) + "\n" \
                        + 'Node occupation is: ' + str(self.occupied)
            else:
                to_return = 'ID: ' + str(self.id) + "\n" \
                            + "Node 1 ID: " + str(self.node1.id) + " " + "Edge 1 ID: " + str(self.edge1.id) + "\n" \
                            + "Node 2 ID: " + str(self.node2.id) + " " + "Edge 2 ID: " + str(self.edge2.id) +"\n" \
                            + "Node 3 ID: " + str(self.node3.id) + " " + "Edge 3 ID: " + str(self.edge3.id) +"\n" \
                            + "Port: " + str(self.port) + "\n" \
                            + 'Node occupation is: ' + str(self.occupied) \
                            + " by " + str(self.player.disp_name)

        return to_return


class Edge:
    def __init__(self, id) -> None:
        self.id = id
        self.occupied = False
        self.player = None


    def occupyEdge(self, player):
        if self.occupied == True:
            return False

        self.occupied = True
        self.player = player
        return True

    def edgeState(self):
        if self.player == None:
            return [0]
        else:
            return [self.player.id]


class Tile:
    def __init__(self, id, value, resource, node1, node2, node3, node4, node5, node6, blocked=False) -> None:
        self.id = id
        self.value = value
        self.resource = resource
        self.nodes = [node1, node2, node3, node4, node5, node6]
        self.blocked = blocked


    def assignResources(self):
        if self.blocked:
            print("Tile is blocked by robber")
            return True
        for n in self.nodes:
            if n.occupied:
                if n.settlement_type == "Settlement":
                    n.player.addResource(self.resource, 1)
                    
                elif n.settlement_type == "City":
                    n.player.addResource(self.resource, 2)

                else:
                    try:
                        print("problem assigning {} to {}".format(self.resource, n.player.disp_name))
                    except:
                        print("No player assigned to node {}".format(n.id))
                    return False

        return True

    def tileState(self):
        to_return = []
        to_return.append(self.value)

        # add resource state
        to_return.append(resource_str_to_num[self.resource])

        # check robbed state
        if self.blocked == False:
            to_return.append(0)
        else:
            to_return.append(1)

        return to_return
        

    def __str__(self) -> str:
        return "ID :" + str(self.id) + "\n" \
                "Value: " + str(self.value) + "\n" \
                "Resource: " +str(self.resource) + "\n" \
                "Blocked: " +str(self.blocked) + "\n" \
                "Node 1: " +str(self.nodes[0].id) + "\n" \
                "Node 2: " +str(self.nodes[1].id) + "\n" \
                "Node 3: " +str(self.nodes[2].id) + "\n" \
                "Node 4: " +str(self.nodes[3].id) + "\n" \
                "Node 5: " +str(self.nodes[4].id) + "\n" \
                "Node 6: " +str(self.nodes[5].id) + "\n"


class Player:
    def __init__(self, id, disp_name, game) -> None:
        self.id = id
        self.disp_name = disp_name

        self.real_vp = 0
        self.perceived_vp = 0

        self.resource = {
            "wool": 0,
            "lumber": 0,
            "grain": 0,
            "ore": 0,
            "brick": 0
        }

        self.settled_nodes = []
        self.settled_edges = []
        self.settled_tiles = []

        self.dev_cards = {
            'Knights': 0,
            'VP': 0,
            'Road Building': 0,
            'Year of Plenty': 0,
            'Monopoly': 0
        }

        self.ports = {
            "wool":0,
            "lumber":0,
            "grain":0,
            "ore":0,
            "brick":0,
            "3-1": 0
        }

        self.largest_army = False
        self.longest_road = False

        self.knight_usage = 0

        # check if player can use dev cards this turn
        self.dev_card_usage = True

        self.game = game


    def addResource(self, type, amount):
        self.resource[type] = self.resource[type] + amount

    def buildRoad(self, edge:Edge) -> bool:
        if (self.resource["brick"] >= 1) and (self.resource["lumber"] >= 1):
            if edge.occupyEdge(self) == False:
                print("A road is already built")
                return False
            self.resource["brick"] = self.resource["brick"] - 1
            self.resource["lumber"] = self.resource["lumber"] - 1
            print(f"{self.disp_name} has built a road")
            return True
        else:
            print(f"{self.disp_name} does not enough resources to build a road")
            return False

    def buildSettlement(self, node:Node) -> bool:
        if (self.resource["brick"] >= 1) and (self.resource["lumber"] >= 1) and (self.resource["wool"] >= 1) and (self.resource["grain"]):
            if node.occupyNode(self) == False:
                return False
            self.resource["brick"] = self.resource["brick"] - 1
            self.resource["lumber"] = self.resource["lumber"] - 1
            self.resource["wool"] = self.resource["wool"] - 1
            self.resource["grain"] = self.resource["grain"] - 1

            print(f"{self.disp_name} has built a settlement")
            if node.port_num != 0:
                self.ports[resource_num_to_str[node.port_num]] = self.ports[resource_num_to_str[node.port_num]] + 1
            self.real_vp = self.real_vp + 1
            self.perceived_vp = self.perceived_vp + 1
            return True
        else:
            print(f"{self.disp_name} does not enough resources to build a settlement")
            return False

    def buildCity(self, node:Node) -> bool:
        if node.occupied == False:
            print("Nothing is built here")
            return False

        if (self.resource["grain"] >= 2) and (self.resource["ore"] >= 3):
            if node.upgradeNode(self) == False:
                return False

            self.resource["grain"] = self.resource["grain"] - 2
            self.resource["ore"] = self.resource["ore"] - 3

            
            print(f"{self.disp_name} has built a city")
            self.real_vp = self.real_vp + 1
            self.perceived_vp = self.perceived_vp + 1
            return True


        else:
            print(f"{self.name} does not enough resources to build a city")
            return False

    # implement dev card purchase (dont forget "cant use card just bought")
    def buyDevCard(self) -> bool:
        if len(self.game.dev_cards) <= 0:
            print("No development cards available to purchase")
            return False

        if (self.resource["grain"] >= 1) and (self.resource["wool"] >= 1) and (self.resource["ore"] >= 1):
            self.resource["wool"] = self.resource["wool"] - 1
            self.resource["grain"] = self.resource["grain"] - 1
            self.resource["ore"] = self.resource["ore"] - 1
            self.dev_card_usage = False
            print("Purchasing Developement Card")
            card = self.game.drawDevCard()
            self.dev_cards[card] = self.dev_cards[card] + 1
            if card == "VP":
                self.real_vp = self.real_vp + 1
            return True
        return False

    
    def useKnight(self, target) -> bool:
        if self.dev_card_usage == False:
            print("Can not use development cards at this time")
            return False
        if self.dev_cards['Knights'] <= 0:
            print("no knights available")
            return False

        if self.game.moveRobber(self, target):
            self.dev_cards['Knights'] = self.dev_cards['Knights'] - 1
            self.game.dev_cards.append("Knights")
            self.dev_card_usage = False
            self.knight_usage = self.knight_usage + 1
            return True
        return False
    

    def useRaodBuilding(self, edge1_id, edge2_id) -> bool:
        if self.dev_card_usage == False:
            print("Can not use development cards at this time")
            return False
        if self.dev_cards['Road Building'] <= 0:
            print("no Road Building available")
            return False

        if self.game.board.edge_all[edge1_id].occupied or self.game.board.edge_all[edge2_id].occupied:
            print("one of the edges is already occupied")
            return False

        self.game.board.edge_all[edge1_id].occupyEdge(self)
        self.game.board.edge_all[edge2_id].occupyEdge(self)
        self.dev_card_usage = False

        return True


    def useYearOfPlenty(self, r1, r2) -> bool:
        if self.dev_card_usage == False:
            print("Can not use development cards at this time")
            return False
        if self.dev_cards['Year of Plenty'] <= 0:
            print("no Year of Plenty available")
            return False

        self.addResource(resource_num_to_str[r1], 1)
        self.addResource(resource_num_to_str[r2], 1)
        self.dev_card_usage = False
        return True

    def useMonopoly(self, resource_num) -> bool:
        if self.dev_card_usage == False:
            print("Can not use development cards at this time")
            return False
        if self.dev_cards['Monopoly'] <= 0:
            print("no Monopoly available")
            return False

        # tally and take resources from all other players
        to_add = 0
        for player in self.game.player_all:
            if self.game.player_all[player] != self:
                to_add = to_add + self.game.player_all[player].resource[resource_num_to_str[resource_num]]
                self.game.player_all[player].resource[resource_num_to_str[resource_num]] = 0
        
        # add resources to self
        self.resource[resource_num_to_str[resource_num]] = self.resource[resource_num_to_str[resource_num]] + to_add

        self.dev_card_usage = False
        return True


    def endTurn(self) -> bool:
        self.dev_card_usage = True

        if self.largest_army == False:
            pass

        if self.longest_road == False:
            pass

        return True
        
class Board:
    # Create graphs needed for board layout
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
    node_edge_graph = {
        1:(1,7),
        2:(1,2),
        3:(2,3,8),
        4:(3,4),
        5:(4,5,9),
        6:(5,6),
        7:(6,10),
        8:(11,19),
        9:(7,11,12),
        10:(12,13,20),
        11:(8,13,14),
        12:(14,15,21),
        13:(9,15,16),
        14:(16,17,22),
        15:(10,17,18),
        16:(18,23),
        17:(24,34),
        18:(19,24,25),
        19:(25,26,35),
        20:(20,26,27),
        21:(27,28,36),
        22:(21,28,29),
        23:(29,30,37),
        24:(22,30,31),
        25:(31,32,38),
        26:(23,32,33),
        27:(33,39),
        28:(34,40),
        29:(40,41,50),
        30:(35,41,42),
        31:(42,43,51),
        32:(36,43,44),
        33:(44,45,52),
        34:(37,45,46),
        35:(46,47,53),
        36:(38,47,48),
        37:(48,49,54),
        38:(39,49),
        39:(50,55),
        40:(55,56,63),
        41:(51,56,57),
        42:(57,58,64),
        43:(52,58,59),
        44:(59,60,65),
        45:(53,60,61),
        46:(61,62,66),
        47:(54,62),
        48:(63,67),
        49:(67,68),
        50:(64,68,69),
        51:(69,70),
        52:(65,70,71),
        53:(71,72),
        54:(66,72)
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

    port_location = [
        (1,2),
        (4,5),
        (15,16),
        (27,38),
        (46,47),
        (51,52),
        (48,49),
        (29,39),
        (8,18)
    ]

    def __init__(self) -> None:
        # place to put class instances related to this game instance
        self.tile_all = []
        self.node_all = []
        self.edge_all = []


        # Work on initailizing the Edges (Roads)
        for i in range (72):
            self.edge_all.append(Edge(i+1))


        # Work on initializing the Nodes (City/Settlement)
        # Initialize nodes
        for k in self.node_graph.keys():
            self.node_all.append(Node(k))

        # connect nodes
        for node in self.node_all:
            node_connections = self.node_graph[node.id]
            i = 0
            for element in node_connections:
                if i == 0:
                    node.node1 = self.node_all[element-1]
                elif i == 1:
                    node.node2 = self.node_all[element-1]
                elif i == 2:
                    node.node3 = self.node_all[element-1]
                else:
                    print("Issues have happened")
                i = i+1
            
            edge_connections = self.node_edge_graph[node.id]
            i = 0
            for element in edge_connections:
                if i == 0:
                    node.edge1 = self.edge_all[element-1]
                elif i == 1:
                    node.edge2 = self.edge_all[element-1]
                elif i == 2:
                    node.edge3 = self.edge_all[element-1]
                else:
                    print("Issues have happened")
                i = i+1


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

            # get corrosponding nodes
            node_list = []
            for n in self.tile_node_graph[random_id]:
                node_list.append(self.node_all[n-1])

            # create Tile
            self.tile_all.append(Tile(random_id, high_val, random_resource,
                                        node_list[0], node_list[1], node_list[2],
                                        node_list[3], node_list[4], node_list[5]))

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
            
            # get corrosponding nodes
            node_list = []
            for n in self.tile_node_graph[random_id]:
                node_list.append(self.node_all[n-1])

            # create Tile
            self.tile_all.append(Tile(random_id, very_low_val, random_resource,
                                        node_list[0], node_list[1], node_list[2],
                                        node_list[3], node_list[4], node_list[5]))

        # add in everything else besides desert
        for low_val in self.low_values:
            random_id = random.choice(self.id)
            random_resource = random.choice(self.resource)

            # remove the random choice
            self.resource.remove(random_resource)
            self.id.remove(random_id)

            # get corrosponding nodes
            node_list = []
            for n in self.tile_node_graph[random_id]:
                node_list.append(self.node_all[n-1])

            self.tile_all.append(Tile(random_id, low_val, random_resource,
                                        node_list[0], node_list[1], node_list[2],
                                        node_list[3], node_list[4], node_list[5]))
        
        # add the desert
        node_list = []
        for n in self.tile_node_graph[self.id[0]]:
            node_list.append(self.node_all[n-1])

        self.blocked_tile_id = self.id[0]

        self.tile_all.append(Tile(self.id[0],7,"desert",
                                node_list[0], node_list[1], node_list[2],
                                node_list[3], node_list[4], node_list[5], True))

        # convert tiles, nodes, and edge list to dict
        self.tile_all = self.pack_id_to_dict(self.tile_all)
        self.node_all = self.pack_id_to_dict(self.node_all)
        self.edge_all = self.pack_id_to_dict(self.edge_all)

        # add ports
        port_num_list = [1,2,3,4,5,6,6,6,6]
        for node_set in self.port_location:
            random_port = random.choice(port_num_list)
            port_num_list.remove(random_port)
            for node in node_set:
                self.node_all[node].assignPort(random_port)


    def pack_id_to_dict(self, list_in:list):
        out = {}
        for l in list_in:
            out[l.id] = l
        
        return out


    def boardState(self):
        to_return = []
        # Iterate over tile state
        for key in range(len(self.tile_all)):
            for val in self.tile_all[key+1].tileState():
                to_return.append(val)
        
        # Iterate over Nodes
        for key in range(len(self.node_all)):
            for val in self.node_all[key+1].nodeState():
                to_return.append(val)

        # Iterate over edges
        for key in range(len(self.edge_all)):
            for val in self.edge_all[key+1].edgeState():
                to_return.append(val)

        return to_return


class Game:
    # store all game instances
    all = []

    def __init__(self, player1name="P1", player2name="P2", player3name="P3", player4name="P4") -> None:
        # State of the game
        self.completed = False

        # store player instances for the game
        self.player_all = {}

        # Initialize Board
        self.board = Board()

        # Work on initalizing the Players

        self.player_all[player1name] = Player(1, player1name, self)
        self.player_all[player2name] = Player(2, player2name, self)
        self.player_all[player3name] = Player(3, player3name, self)
        self.player_all[player4name] = Player(4, player4name, self)

        
        # Initialize Dev Cards
        self.dev_cards = []
        for i in range(5):
            self.dev_cards.append("VP")
        
        for i in range(14):
            self.dev_cards.append("Knights")

        for i in range(2):
            self.dev_cards.append("Road Building")

        for i in range(2):
            self.dev_cards.append("Year of Plenty")

        for i in range(2):
            self.dev_cards.append("Monopoly")

        #randomize turn order
        self.turn_order = [player1name, player2name, player3name, player4name]
        random.shuffle(self.turn_order)

        # Append instance of game to class variable
        Game.all.append(self)


    def drawDevCard(self):
        chosen_card = random.choice(self.dev_cards)
        self.dev_cards.remove(chosen_card)
        return chosen_card

    def rollDice(self):
        return randint(1,7)+randint(1,7)

    def distributeResources(self, roll):
        for tile in self.board.tile_all:
            if tile.value == roll:
                tile.assignResources()

    def moveRobber(self, tile_id, initial_player:Player, effected_player:Player):
        if initial_player == effected_player:
            print("You can not rob yourself")
            return False
        list_of_players = []
        for node in self.board.tile_all[tile_id].nodes:
            if (node.player in list_of_players) == False:
                list_of_players.append(node.player)
        if (effected_player in list_of_players) == False:
            print("you can not rob this player")
            return False
            
        self.board.tile_all[self.board.blocked_tile_id].blocked = False
        self.board.tile_all[tile_id].blocked = True

        player_resources = []
        for i in range(5):
            repeater = effected_player.resource[resource_num_to_str[i+1]]
            for j in range(repeater):
                player_resources.append(i+1)
        random_steal = random.choice(player_resources)

        effected_player.addResource(resource_str_to_num[random_steal], -1)
        initial_player.addResource(resource_str_to_num[random_steal], 1)
        return True
        

    # Implement trading
    # should randomize who gets to trade first






# %%

