import random
from helper_dicts import *
from player import *

# Define the nodes each settlement is on using the node_graph dictionary from helper_dict.py
class Node:
    def __init__(self, id, node_connections, edge_connections):
        self.id = id                                # Unique node ID
        self.owner = None                           # Player ID
        self.settlement_type = 0                    # 0 for no settlement, 1 for settlement, 2 for city
        self.node_connections = node_connections    # Tuple of connected nodes
        self.edge_connections = edge_connections    # Tuple of connected edges
        self.port = None                            # Port type
        
    # check if the node has a settlement or city on it
    def has_building(self):
        if self.settlement_type != 0:
            return True
        return False
    
        
# Set up the edges between the nodes representing the roads using node_edge_graph from helper_dict.py
class Edge:
    def __init__(self, id, edges, nodes):
        self.id = id                                # Unique edge ID
        self.owner = None                           # Player ID
        self.edges = edges                          # Tuple of connected edges
        self.nodes = nodes                          # Tuple of connected nodes
        
        
        
# Define the tiles on the board using the tile_graph dictionary from helper_dict.py
class Tile:
    def __init__(self, id, nodes):
        self.id = id                                # Tile ID
        self.nodes = nodes                          # Tuple of connected nodes
        self.resource = None                        # Resource type
        self.number = None                          # Resource value
        self.robber = 0                             # boolean for the existance of robber
        
    # set the resource attribute to the resource type of the tile
    def set_resource(self, resource):
        self.resource = resource
    
    # set the number attribute to the number on the tile
    def set_number(self, number):
        self.number = number
        
        
# Create the board class which will contain all the nodes, edges, and tiles
class Board:
    # Initialize the board and create the nodes, edges, and tiles using the helper dictionaries
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players 

        # Create the nodes
        self.nodes = {}
        for node_id in node_graph:
            self.nodes[node_id] = Node(node_id, node_graph[node_id], node_edge_graph[node_id])
        
        # make a copy of the port_types dictionary from helper_dict.py
        port_types_copy = port_types.copy()

        # Set the ports of the nodes using the port_location dictionary from helper_dict.py
        for nodes in port_location:
            # randomly sample a port type from the port_types_copy list
            port = random.sample(port_types_copy, 1)[0]
            port_types_copy.remove(port)
            # set the port attribute of the nodes in the port_location dictionary to the port type
            for node in nodes:
                self.nodes[node].port = port
            
        # Create the edges
        self.edges = {}
        for edge_id in edge_graph:
            self.edges[edge_id] = Edge(edge_id, edge_graph[edge_id], edge_node_graph[edge_id])
            
        # Create the tiles
        self.tiles = {}
        for tile_id in tile_node_graph:
            self.tiles[tile_id] = Tile(tile_id, tile_node_graph[tile_id])
            
        # copy tile_resource and tile_values to avoid changing the original lists
        tile_resource_copy = tile_resource.copy()
        tile_values_copy = tile_values.copy()
            
        # Set the resources and values of the tiles randomly sampled without replacement using the tile_resource and tile_values lists from helper_dict.py.
        for tile in self.tiles.values():
            # randomly sample a resource from the tile_resource list
            resource = random.sample(tile_resource_copy, 1)[0]
            tile.set_resource(resource)
            tile_resource_copy.remove(resource)
            # if the resource is desert, set the robber attribute to True
            if resource == "desert":
                tile.robber = True
                # also set the value of the tile to 0
                tile.set_number(0)
            
        # Setting the tile_values is a bit more complicated because the tile values restrict the number 2 and 12 from being adjacent to each other and 6 and 8 from being adjacent to each other. First randomly assign the 2 and 12 to the tiles. Then randomly assign the 6 and 8 to the tiles. Then randomly assign the remaining values to the tiles.
        # Set the 2 and 12 using the first element of the tile_values list.
        for value in tile_values_copy[0]: # retrieve the 2 and 12 from the first element of the tile_values list
            # randomly sample a tile from the tiles list and check if the tile has a value assigned to it. If it does not, assign the value to the tile. Also check if the tile has a 2 or 12 assigned adjacent to it. If it does not, assign the value to the tile. This is done in a while loop until the value is assigned to a tile. Use the tile_graph dictionary to check if the tile has a 2 or 12 assigned adjacent to it.
            while True:
                tile = random.sample(list(self.tiles.values()), 1)[0]
                if tile.number is None and value not in tile_graph[tile.id]:
                    tile.set_number(value)
                    break
                
        # Set the 6 and 8 using the second element of the tile_values list.
        for value in tile_values_copy[1]:
            while True:
                tile = random.sample(list(self.tiles.values()), 1)[0]
                if tile.number is None and value not in tile_graph[tile.id]:
                    tile.set_number(value)
                    break
        
        # Set the remaining values using the third element of the tile_values list. This can be done without any restrictions.
        for value in tile_values_copy[2]:
            while True:
                tile = random.sample(list(self.tiles.values()), 1)[0]
                if tile.number is None:
                    tile.set_number(value)
                    break
                
        # hold setup phase
        self.setup_phase = True
        
        # Initialize some game components
        self.robber_tile = None
        self.robber_moved = False
        self.longest_road_amount = 3
        self.longest_road_player = None
        self.largest_army_amount = 3
        self.largest_army_player = None
        self.dice_roll = None
        
        # set up development cards
        self.development_cards = []
        for i in range(5):
            self.development_cards.append("victory_point")

        for i in range(14):
            self.development_cards.append("knights")

        for i in range(2):
            self.development_cards.append("road_building")

        for i in range(2):
            self.development_cards.append("year_of_plenty")

        for i in range(2):
            self.development_cards.append("monopoly")
        
        # set up the players
        self.players = []
        for player_num in range(self.number_of_players):
            self.players.append(Player(player_num))

        print("the player len is: ", len(self.players))
            
                        
    # Display the board in a graphical format. Include the nodes, edges, tiles, settlements, cities, roads, resources, numbers, and robber
    def display_board(self):
        # Create a dictionary to store the information to be displayed
        display_dict = {"Nodes":{}, "Edges":{}, "Tiles":{}}
        
        # Add the nodes to the dictionary
        for node in self.nodes.values():
            display_dict["Nodes"][node.id] = {"settlement": node.settlement_type}
        
        # Add the edges to the dictionary
        for edge in self.edges.values():
            display_dict["Edges"][edge.id] = {"road": edge.road}
        
        # Add the tiles to the dictionary
        for tile in self.tiles.values():
            display_dict["Tiles"][tile.id] = {"resource": tile.resource, "number": tile.number, "robber": tile.robber}
        
        # Print the dictionary
        # pprint(display_dict)
        return display_dict
    
