# This project aims to create a python implementation of the board game Settlers of Catan to be playable by an artificial agent

# %%
import random
from numpy.random import randint
import copy
from helper_dicts import *


class Node:
    """
    This class contains the structure for nodes/settlements

    Variables
    ---------
    self.id: [int] A unique ID value which represents the position on the board
    self.nodes: [list] contains a list of connected nodes
    self.edges: [list] contains a list of connected edges
    self.occupied: [bool] is the node occupied
    self.settlement_type: [str] what kind of settlement
    self.player: [Player] player who occupies the node
    self.port: [str] type of the port if there is one, None otherwise
    self.port_num: [int] the resource number corresponding to the port type, 0 if there is no port

    Methods
    -------
    __init__(self, id, node1=None, node2=None, node3=None, edge1=None, edge2=None, edge3=None)
        Initializes a Node object
    getConnections(self)
        Returns the ids of the nodes connected to this node
    occupyNode(self, player)
        Occupies this node with a settlement
    upgradeNode(self, player)
        Upgrades the settlement on this node to a city
    assignPort(self, port_type)
        Assigns a port to this node of the given type
    nodeState(self)
        Returns the state of this node as a list of integers
    __str__(self)
        Returns a string representation of this node
    """

    def __init__(self, id, node1=None, node2=None, node3=None, edge1=None, edge2=None, edge3=None) -> None:
        """
        Initializes a Node object

        Parameters
        ----------
        id : int
            A unique ID value which represents the position on the board
        node1, node2, node3 : Node
            The nodes connected to this node
        edge1, edge2, edge3 : Edge
            The edges connected to this node
        """
        self.id = id

        self.nodes = [node1, node2, node3]
        self.edges = [edge1, edge2, edge3]

        self.occupied = False
        self.settlement_type = ""
        self.player = None

        self.port = None
        self.port_num = 0

    def getConnections(self):
        """
        Returns the ids of the nodes connected to this node

        Returns
        -------
        tuple of int
            The ids of the nodes connected to this node
        """
        
        if (self.node3 == None):
            return (self.id, self.node1.getID(), self.node2.getID())
        else:
            return (self.id, self.node1.getID(), self.node2.getID(), self.node3.getID())

    def occupyNode(self, player):
        """
        Occupies this node with a settlement

        Parameters
        ----------
        player : Player
            The player who is occupying the node

        Returns
        -------
        bool
            True if the node was successfully occupied, False otherwise
        """
        if self.player == None:
            pass
        elif self.player.id != player.id:
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
        """
        This method upgrades the node from a Settlement to a City

        Parameters
        ----------
        player: [Player] the player who is upgrading the node

        Returns
        -------
        bool: True if upgrade is successful, False otherwise
        """

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
        """
        This method assigns a port to the node

        Parameters
        ----------
        port_type: [int] the type of port to assign (1-6)

        Returns
        -------
        bool: True if port is assigned successfully, False otherwise
        """
        
        self.port_num = port_type
        if port_type >= 1 and port_type <= 6:
            self.port = resource_num_to_str[port_type]
        else:
            print("Problem assigning port with type {}".format(port_type))
            self.port_num = 0
            return False
        return True

    def nodeState(self):
        """
        This method returns the current state of the node in a list format

        Returns
        -------
        list: [int, int, int] representing the discretized state of the node
            - the first int represents the settlement type (0 for none, 1 for settlement, 2 for city)
            - the second int represents the player ID (0 for unoccupied)
            - the third int represents the port type (0 for no port)
        """
        
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

        # Discretize port state
        to_return.append(self.port_num)

        return to_return

    def __str__(self) -> str:
        to_return = 'ID: {} \n'.format(str(self.id))
        for i in range(3):
            if self.nodes[i] == None or self.edges[i] == None:
                break
            to_return += "Node {} ID: {} Edge {} ID: {}\n".format(
                str(i+1), str(self.nodes[i].id), str(i+1), str(self.edges[i].id))

        to_return += "Port: {}\n".format(str(self.port)) \
            + "Occupation statue: {}".format(str(self.occupied))

        return to_return


class Edge:
    """
    This class contains the structure for edges/roads

    Variables
    ---------
    self.id: [int] A unique ID value which represents the position on the board
    self.occupied: [bool] is the edge occupied
    self.player: [Player] player who occupies the edge

    Methods
    -------
    __init__(self, id)
    occupyEdge(self, player)
        Attempts to occupy an edge with the player object provided. Returns True if successful, False otherwise.
    edgeState(self)
        Returns a list containing the ID of the occupying player, or 0 if unoccupied.
    __str__(self)
        Returns a string representation of the edge object.
    """
    
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
        to_return = []

        if self.player == None:
            to_return.append(0)
            return to_return
        else:
            to_return.append(self.player.id)
            return to_return

    def __str__(self) -> str:
        to_return = ""
        to_return += "ID: {}\n".format(str(self.id)) \
            + "Occupation: {}\n".format(str(self.occupied))
        if self.player == None:
            to_return += "Player: None"
        else:
            to_return += "Player: {}".format(str(self.player.disp_name))

        return to_return


class Tile:
    """
    The Tile class represents a tile on the board.

    Attributes:
        id (int): The unique ID of the tile.
        value (int): The number that must be rolled to collect resources from this tile.
        resource (str): The type of resource that the tile provides.
        nodes (list of Node objects): The six nodes that make up the corners of the tile.
        blocked (bool): Indicates whether the tile is blocked by the robber.

    Methods:
        assignResources():
            If the tile is not blocked by the robber, assigns the appropriate amount of resources to each player
            with a settlement or city on one of the tile's nodes. Returns True if successful, False otherwise.

        tileState():
            Returns a list representing the state of the tile, including its value, resource type, and whether it
            is currently blocked by the robber.

        __str__():
            Returns a string representation of the tile, including its ID, value, resource type, and the IDs of its nodes.
    """
    
    def __init__(self, id, value, resource, node1, node2, node3, node4, node5, node6, blocked=False) -> None:
        """
        Initializes a new Tile object.

        Args:
            id (int): The unique ID of the tile.
            value (int): The number that must be rolled to collect resources from this tile.
            resource (str): The type of resource that the tile provides.
            node1 (Node object): The first node that makes up a corner of the tile.
            node2 (Node object): The second node that makes up a corner of the tile.
            node3 (Node object): The third node that makes up a corner of the tile.
            node4 (Node object): The fourth node that makes up a corner of the tile.
            node5 (Node object): The fifth node that makes up a corner of the tile.
            node6 (Node object): The sixth node that makes up a corner of the tile.
            blocked (bool): Indicates whether the tile is blocked by the robber.
        """
        self.id = id
        self.value = value
        self.resource = resource
        self.nodes = [node1, node2, node3, node4, node5, node6]
        self.blocked = blocked

    def assignResources(self):
        """
        If the tile is not blocked by the robber, assigns the appropriate amount of resources to each player
        with a settlement or city on one of the tile's nodes. Returns True if successful, False otherwise.
        """
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
                        print("problem assigning {} to {}".format(
                            self.resource, n.player.disp_name))
                    except:
                        print("No player assigned to node {}".format(n.id))
                    return False

        return True

    def tileState(self):
        """
        Returns a list representing the state of the tile, including its value, resource type, and whether it
        is currently blocked by the robber.
        """
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
            "Resource: " + str(self.resource) + "\n" \
            "Blocked: " + str(self.blocked) + "\n" \
            "Node 1: " + str(self.nodes[0].id) + "\n" \
            "Node 2: " + str(self.nodes[1].id) + "\n" \
            "Node 3: " + str(self.nodes[2].id) + "\n" \
            "Node 4: " + str(self.nodes[3].id) + "\n" \
            "Node 5: " + str(self.nodes[4].id) + "\n" \
            "Node 6: " + str(self.nodes[5].id) + "\n"


class Player:
    """
    A class to represent a player in the game of Settlers of Catan.

    Attributes
    ----------
    disp_name : str
        The name of the player.
    game : Game
        The game object that the player belongs to.
    color : str
        The color of the player's game piece.
    resource : dict
        A dictionary containing the player's current resources. Keys are resource types ('brick', 'wood', 'sheep', 'wheat', 'ore') and values are the corresponding integer amounts.
    dev_cards : dict
        A dictionary containing the player's current development cards. Keys are card types ('Knight', 'Victory Point', 'Road Building', 'Year of Plenty', 'Monopoly') and values are the corresponding integer amounts.
    real_vp : int
        The number of victory points that the player has earned through building settlements, cities, and other means.
    dev_card_usage : bool
        A boolean indicating whether the player has already used a development card during their turn.
    knight_usage : int
        The number of times the player has played a Knight card and earned the Largest Army special victory point.
    longest_road : bool
        A boolean indicating whether the player currently has the longest road and earned the Longest Road special victory point.
    largest_army : bool
        A boolean indicating whether the player currently has the largest army and earned the Largest Army special victory point.

    Methods
    -------
    addResource(resource_type: str, amount: int) -> None:
        Add a specified amount of a resource to the player's current resources.
    removeResource(resource_type: str, amount: int) -> bool:
        Remove a specified amount of a resource from the player's current resources. Returns True if successful, False otherwise.
    buildSettlement(intersection_id: int, initial: bool = False) -> bool:
        Build a settlement on a specified intersection. Returns True if successful, False otherwise.
    buildCity(intersection_id: int) -> bool:
        Upgrade a settlement to a city on a specified intersection. Returns True if successful, False otherwise.
    buildRoad(edge_id: int) -> bool:
        Build a road on a specified edge. Returns True if successful, False otherwise.
    buyDevCard() -> bool:
        Purchase a random development card from the game's deck. Returns True if successful, False otherwise.
    useKnight(target: int) -> bool:
        Use a Knight card to move the robber to a specified tile. Returns True if successful, False otherwise.
    useRoadBuilding(edge1_id: int, edge2_id: int) -> bool:
        Use a Road Building card to build two roads on specified edges. Returns True if successful, False otherwise.
    useYearOfPlenty(r1: int, r2: int) -> bool:
        Use a Year of Plenty card to gain two resources of specified types. Returns True if successful, False otherwise.
    useMonopoly(resource_num: int) -> bool:
        Use a Monopoly card to take all of a specified resource type from all other players and add it to the player's current resources. Returns True if successful, False otherwise.
    endTurn() -> bool:
        Ends the player's turn and updates any necessary state information.
    """

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
            "wool": 0,
            "lumber": 0,
            "grain": 0,
            "ore": 0,
            "brick": 0,
            "3-1": 0
        }

        self.largest_army = False
        self.longest_road = False

        self.knight_usage = 0

        # check if player can use dev cards this turn
        self.dev_card_usage = True

        # check total cards
        self.total_cards = 0
        
        self.game = game

    def addResource(self, type, amount):
        self.resource[type] = self.resource[type] + amount

    def calculate_total_cards(self):
        self.total_cards = self.resource["wool"] + self.resource["lumber"] + \
            self.resource["grain"] + \
            self.resource["ore"] + self.resource["brick"]
        return self.total_cards

    def buildRoad(self, edge: Edge) -> bool:
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

    def buildSettlement(self, node: Node) -> bool:
        if (self.resource["brick"] >= 1) and (self.resource["lumber"] >= 1) and (self.resource["wool"] >= 1) and (self.resource["grain"]):
            if node.occupyNode(self) == False:
                return False
            self.resource["brick"] = self.resource["brick"] - 1
            self.resource["lumber"] = self.resource["lumber"] - 1
            self.resource["wool"] = self.resource["wool"] - 1
            self.resource["grain"] = self.resource["grain"] - 1

            print(f"{self.disp_name} has built a settlement")
            if node.port_num != 0:
                self.ports[resource_num_to_str[node.port_num]
                           ] = self.ports[resource_num_to_str[node.port_num]] + 1
            self.real_vp = self.real_vp + 1
            self.perceived_vp = self.perceived_vp + 1
            return True
        else:
            print(f"{self.disp_name} does not enough resources to build a settlement")
            return False

    def buildCity(self, node: Node) -> bool:
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
        # if len(self.game.dev_cards) <= 0:
        #     print("No development cards available to purchase")
        #     return False

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
        
        if self.game.board.tile_all[target].blocked == False:
            print("Tile is already blocked")
            return False

        if self.game.moveRobber(self, target):
            self.dev_cards['Knights'] = self.dev_cards['Knights'] - 1
            self.game.dev_cards.append("Knights")
            self.dev_card_usage = False
            self.knight_usage = self.knight_usage + 1
            
            for t in self.game.board.tile_all.values():
                t.blocked = False
            
            self.game.board.tile_all[target].blocked = True
            
            return True
        
        return False

    def useRoadBuilding(self, edge1_id, edge2_id) -> bool:
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
                to_add = to_add + \
                    self.game.player_all[player].resource[resource_num_to_str[resource_num]]
                self.game.player_all[player].resource[resource_num_to_str[resource_num]] = 0

        # add resources to self
        self.resource[resource_num_to_str[resource_num]
                      ] = self.resource[resource_num_to_str[resource_num]] + to_add

        self.dev_card_usage = False
        return True

    def endTurn(self) -> bool:
        self.dev_card_usage = True

        if self.largest_army == False:
            pass

        if self.longest_road == False:
            pass

        return True

    def publicPlayerState(self) -> list:
        to_return = []
        to_return.append(self.id)
        to_return.append(self.real_vp)
        to_return.append(self.perceived_vp)
        to_return.append(self.total_cards)
        to_return.append(self.knight_usage)
        to_return.append(self.ports["wool"])
        to_return.append(self.ports["lumber"])
        to_return.append(self.ports["grain"])
        to_return.append(self.ports["ore"])
        to_return.append(self.ports["brick"])
        to_return.append(self.ports["3-1"])

        return to_return

    def privatePlayerState(self) -> list:
        to_return = self.publicPlayerState()

        # resources
        to_return.append(self.resource["wool"])
        to_return.append(self.resource["lumber"])
        to_return.append(self.resource["grain"])
        to_return.append(self.resource["ore"])
        to_return.append(self.resource["brick"])

        # dev_cards
        to_return.append(self.dev_cards['Knights'])
        to_return.append(self.dev_cards['VP'])
        to_return.append(self.dev_cards['Road Building'])
        to_return.append(self.dev_cards['Year of Plenty'])
        to_return.append(self.dev_cards['Monopoly'])

        if self.dev_card_usage == True:
            to_return.append(1)
        else:
            to_return.append(0)

        return to_return


class Board:
    """
    Represents a game board for Settlers of Catan.

    Attributes:
        tile_all (dict): A dictionary containing all the tiles on the board,
                         indexed by tile ID.
        node_all (dict): A dictionary containing all the nodes (settlements/cities)
                         on the board, indexed by node ID.
        edge_all (dict): A dictionary containing all the edges (roads) on the board,
                         indexed by edge ID.
        longest_road (int): The length of the longest continuous road on the board.
        largest_army (int): The size of the largest army on the board.
        blocked_tile_id (int): The ID of the tile that represents the desert and is
                               not meant to be assigned a resource or a number value.

    Methods:
        __init__(): Initializes the board by creating all the tiles, nodes, and edges,
                    and connecting them together. Also assigns random resources and
                    number values to the tiles.
        pack_id_to_dict(lst): Takes a list of objects and packs them into a dictionary
                              indexed by their ID attribute.
    """

    def __init__(self) -> None:
        # place to put class instances related to this game instance
        self.tile_all = []
        self.node_all = []
        self.edge_all = []

        # player with the longest road/largest army
        self.longest_road = 0
        self.largest_army = 0

        # Work on initailizing the Edges (Roads)
        for i in range(72):
            self.edge_all.append(Edge(i+1))

        # Work on initializing the Nodes (City/Settlement)
        # Initialize nodes
        for k in node_graph.keys():
            self.node_all.append(Node(k))

        # connect nodes
        for node in self.node_all:
            node_connections = node_graph[node.id]
            i = 0
            for element in node_connections:
                node.nodes[i] = self.node_all[element-1]
                i = i+1

            edge_connections = node_edge_graph[node.id]
            i = 0
            for element in edge_connections:
                node.edges[i] = self.edge_all[element-1]
                i = i+1

        # work on initializing the Tiles
        self.values = [2, 3, 3, 4, 4, 5, 5, 6,
                       6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        self.resource = ["brick", "brick", "brick",
                         "ore", "ore", "ore",
                         "wool", "wool", "wool", "wool",
                         "grain", "grain", "grain", "grain",
                         "lumber", "lumber", "lumber", "lumber"
                         ]
        self.id = []
        self.available_id = []
        for val in range(19):
            self.id.append(val+1)
            self.available_id.append(val+1)

        self.high_values = [6, 6, 8, 8]
        self.low_values = [3, 3, 4, 4, 5, 5, 9, 9, 10, 10, 11, 11]
        self.very_low_values = [2, 12]

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
            for graph_val in tile_graph[random_id]:
                if graph_val in self.available_id:
                    self.available_id.remove(graph_val)

            # get corrosponding nodes
            node_list = []
            for n in tile_node_graph[random_id]:
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
            for graph_val in tile_graph[random_id]:
                if graph_val in self.available_id:
                    self.available_id.remove(graph_val)

            # get corrosponding nodes
            node_list = []
            for n in tile_node_graph[random_id]:
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
            for n in tile_node_graph[random_id]:
                node_list.append(self.node_all[n-1])

            self.tile_all.append(Tile(random_id, low_val, random_resource,
                                      node_list[0], node_list[1], node_list[2],
                                      node_list[3], node_list[4], node_list[5]))

        # add the desert
        node_list = []
        for n in tile_node_graph[self.id[0]]:
            node_list.append(self.node_all[n-1])

        self.blocked_tile_id = self.id[0]

        self.tile_all.append(Tile(self.id[0], 7, "desert",
                                  node_list[0], node_list[1], node_list[2],
                                  node_list[3], node_list[4], node_list[5], True))

        # convert tiles, nodes, and edge list to dict
        self.tile_all = self.pack_id_to_dict(self.tile_all)
        self.node_all = self.pack_id_to_dict(self.node_all)
        self.edge_all = self.pack_id_to_dict(self.edge_all)

        # add ports
        port_num_list = [1, 2, 3, 4, 5, 6, 6, 6, 6]
        for node_set in port_location:
            random_port = random.choice(port_num_list)
            port_num_list.remove(random_port)
            for node in node_set:
                self.node_all[node].assignPort(random_port)

    def pack_id_to_dict(self, list_in: list) -> dict:
        out = {}
        for l in list_in:
            out[l.id] = l
        return out

    def boardState(self) -> list:
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

        to_return.append(self.longest_road)
        to_return.append(self.largest_army)
        return to_return

class Game:
    """
    The Game class represents an instance of the Settlers of Catan game.

    Attributes:
    - completed (bool): Indicates whether the game has ended or not.
    - player_all (dict): Dictionary containing all Player instances in the game.
    - board (Board): Instance of the Board class representing the game board.
    - dev_cards (list): List of development cards in the game.
    - turn_order (list): List representing the order of player turns in the game.

    Methods:
    - __init__(self, player1name="P1", player2name="P2", player3name="P3", player4name="P4"): Initializes a new instance of the Game class with default or specified player names.
    - drawDevCard(self) -> str: Draws a random development card from the deck.
    - rollDice(self) -> int: Rolls two dice and returns the sum.
    - distributeResources(self, roll): Distributes resources to players based on the roll of the dice.
    - moveRobber(self, tile_id, initial_player: Player, effected_player: Player) -> bool: Moves the robber to the specified tile, and robs a random resource from the specified player.
    - copyGame(self): Returns a deep copy of the current game instance.
    - gameState(self, player: Player): Returns a list of the current game state, including board and player information visible to the specified player.
    """

    def __init__(self, goal, player1name="P1", player2name="P2", player3name="P3", player4name="P4") -> None:
        # State of the game
        self.completed = False
        self.goal = goal

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
            
        self.player_actions = {}
        for p in self.player_all:
            self.player_actions[p] = self.getActions(self.player_all[p])

        # randomize turn order
        self.turn_order = [player1name, player2name, player3name, player4name]
        random.shuffle(self.turn_order)
        
        """
        f = False
        while self.completed == False:
            for p in self.turn_order:
                p.make_move()
                f = self.checkComplete()
                if f == True:
                    break
        """

    def drawDevCard(self) -> str:
        chosen_card = random.choice(self.dev_cards)
        self.dev_cards.remove(chosen_card)
        return chosen_card

    def rollDice(self) -> int:
        return randint(1, 7)+randint(1, 7)

    def distributeResources(self, roll):
        for tile in self.board.tile_all.values():
            if tile.value == roll:
                tile.assignResources()

    def moveRobber(self, tile_id, initial_player: Player, effected_player: Player) -> bool:
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

    def copyGame(self):
        return copy.deepcopy(self)

    def gameState(self, player: Player):
        to_return = self.board.boardState()

        l = player.privatePlayerState()
        for i in l:
            to_return.append(i)

        for p in self.player_all:
            l = self.player_all[p].publicPlayerState()
            for i in l:
                to_return.append(i)

        return to_return

    # Implement trading
    # should randomize who gets to trade first
    def trade(self, offerer: Player, receiver: Player, offer: dict[str, int], request: dict[str, int]) -> bool:
        """
        Trade method allows a player to offer resources to another player in exchange for resources they desire.
        If the trade is valid and accepted, the resources are exchanged between the players.

        Args:
            offerer (Player): The player offering the trade.
            receiver (Player): The player receiving the trade.
            offer (Dict[str, int]): A dictionary representing the resources the offerer is offering. 
                                    Key is the resource name (e.g. "wood"), and value is the quantity.
            request (Dict[str, int]): A dictionary representing the resources the offerer is requesting. 
                                    Key is the resource name (e.g. "brick"), and value is the quantity.

        Returns:
            bool: True if the trade is successful, False otherwise.
        """
        if offerer == receiver:
            print("Can not trade with yourself")
            return False
        
        # Check if offerer and receiver are valid players
        if offerer not in self.player_all.values() or receiver not in self.player_all.values():
            print("Invalid players")
            return False

        # Check if offerer has the resources to offer
        for resource_name, quantity in offer.items():
            if offerer.resource[resource_name] < quantity:
                print(f"{offerer.disp_name} doesn't have enough {resource_name} to trade")
                return False

        # Check if receiver has the resources to trade
        for resource_name, quantity in request.items():
            if receiver.resource[resource_name] < quantity:
                print(f"{receiver.disp_name} doesn't have enough {resource_name} to trade")
                return False

        # Make the trade
        for resource_name, quantity in offer.items():
            offerer.addResource(resource_name, -quantity)
            receiver.addResource(resource_name, quantity)
        for resource_name, quantity in request.items():
            offerer.addResource(resource_name, quantity)
            receiver.addResource(resource_name, -quantity)

        print(f"{offerer.disp_name} trades {offer} to {receiver.disp_name} for {request}")
        return True
    
    def checkComplete(self):
        for p in self.player_all.values:
            if p.real_vp >= self.goal:
                self.completed = True
                print(f"{p.disp_name} has won")
                return True
        
    
    def getActions(self, player: Player):
        self.actions = {}

        val = 0
        # construct settlements
        for i in range(54):
            node = i+1
            self.actions[val] = player.buildSettlement(self.board.node_all[node])
            val += 1
            
        #construct cities
        for i in range(54):
            node = i+1
            self.actions[val] = player.buildCity(self.board.node_all[node])
            val += 1
        
        # construct roads
        for i in range(72):
            edge = i+1
            self.actions[val] = player.buildRoad(self.board.edge_all[edge])
            val += 1
            
        # buy dev card
        self.actions[val] = player.buyDevCard()
        val += 1
        
        # use useKnight
        for i in range(19):
            tile = i + 1
            self.actions[val] = player.useKnight(tile)
            val += 1
        
        # use useRoadBuilding
        for i in range(54):
            t1 = i + 1
            for j in range(54):
                t2 = j + 1
                if t1 != t2:
                    self.actions[val] = player.useRoadBuilding(t1,t2)
                    val += 1
                    
        # use useYearOfPlenty
        for i in range(5):
            r1 = i+1
            for j in range(5):
                r2 = j+1
                self.actions[val] = player.useYearOfPlenty(r1,r2)
                val += 1
                
        # use useMonopoly
        for i in range(5):
            r1 = i+1
            self.actions[val] = player.useMonopoly(r1)
            val += 1
            
        # use endTurn
        self.actions[val] = player.endTurn()

        
# %%

game = Game(10)

print(game.player_all["P1"].resource)
print(game.player_all["P2"].resource)
print(game.player_all["P3"].resource)
print(game.player_all["P4"].resource)

for i in game.board.node_all.values():
    i.occupyNode(game.player_all["P1"])

r = game.rollDice()
print(r)
game.distributeResources(r)

print(game.player_all["P1"].resource)
print(game.player_all["P2"].resource)
print(game.player_all["P3"].resource)
print(game.player_all["P4"].resource)

print(game.player_actions)

# %%
