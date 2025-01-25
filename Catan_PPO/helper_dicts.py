"""
Dictionary for quick conversions between resource strings and their corresponding integer values.

resource_num_to_str: dict
    A dictionary that maps integer values to corresponding resource strings.
    The keys are integers and the values are strings.
    Example: {1: "wool", 2: "lumber", 3: "grain", 4: "ore", 5: "brick", -1: "desert", 6: "3-1"}

resource_str_to_num: dict
    A dictionary that maps resource strings to corresponding integer values.
    The keys are strings and the values are integers.
    Example: {"wool": 1, "lumber": 2, "grain": 3, "ore": 4, "brick": 5, "desert": -1, "3-1": 6}
"""

resource_num_to_str = {
    1: "wool",  # assign the integer value 1 to the string "wool"
    2: "lumber",  # assign the integer value 2 to the string "lumber"
    3: "grain",  # assign the integer value 3 to the string "grain"
    4: "ore",  # assign the integer value 4 to the string "ore"
    5: "brick",  # assign the integer value 5 to the string "brick"
    -1: "desert",  # assign the integer value -1 to the string "desert"
    6: "3-1"  # assign the integer value 6 to the string "3-1"
}

resource_str_to_num = {
    "wool": 1,  # assign the string "wool" to the integer value 1
    "lumber": 2,  # assign the string "lumber" to the integer value 2
    "grain": 3,  # assign the string "grain" to the integer value 3
    "ore": 4,  # assign the string "ore" to the integer value 4
    "brick": 5,  # assign the string "brick" to the integer value 5
    "desert": -1,  # assign the string "desert" to the integer value -1
    "3-1": 6  # assign the string "3-1" to the integer value 6
}

# Create graphs needed for board layout

# Graph of the tiles and their corresponding tiles
tile_graph = {
    1: (2, 4, 5),
    2: (1, 3, 5, 6),
    3: (2, 6, 7),
    4: (1, 5, 8, 9),
    5: (1, 2, 4, 6, 9, 10),
    6: (2, 3, 5, 7, 10, 11),
    7: (3, 6, 11, 12),
    8: (4, 9, 13),
    9: (4, 5, 8, 10, 13, 14),
    10: (4, 5, 9, 11, 14, 15),
    11: (6, 7, 10, 12, 15, 16),
    12: (7, 11, 16),
    13: (8, 9, 14, 17),
    14: (9, 10, 13, 15, 17, 18),
    15: (10, 11, 14, 16, 18, 19),
    16: (11, 12, 15, 19),
    17: (13, 14, 18),
    18: (14, 15, 17, 19),
    19: (15, 16, 18)
}

# Graph of the nodes and the adjacent nodes
node_graph = {
    1: (2, 9),
    2: (1, 3),
    3: (2, 4, 11),
    4: (3, 5),
    5: (4, 6, 13),
    6: (5, 7),
    7: (6, 15),
    8: (9, 18),
    9: (1, 8, 10),
    10: (9, 11, 20),
    11: (3, 10, 12),
    12: (11, 13, 22),
    13: (5, 12, 14),
    14: (13, 15, 24),
    15: (7, 14, 16),
    16: (15, 26),
    17: (18, 28),
    18: (8, 17, 19),
    19: (18, 20, 30),
    20: (10, 19, 21),
    21: (20, 22, 32),
    22: (12, 21, 23),
    23: (22, 24, 34),
    24: (14, 23, 25),
    25: (24, 26, 36),
    26: (16, 25, 27),
    27: (26, 38),
    28: (17, 29),
    29: (28, 30, 39),
    30: (19, 29, 31),
    31: (30, 32, 41),
    32: (21, 31, 33),
    33: (32, 34, 43),
    34: (23, 33, 35),
    35: (34, 36, 45),
    36: (25, 35, 37),
    37: (36, 38, 47),
    38: (27, 37),
    39: (29, 40),
    40: (39, 41, 48),
    41: (31, 40, 42),
    42: (41, 43, 50),
    43: (33, 42, 44),
    44: (43, 45, 52),
    45: (35, 44, 46),
    46: (45, 47, 54),
    47: (37, 46),
    48: (40, 49),
    49: (48, 50),
    50: (42, 49, 51),
    51: (50, 52),
    52: (44, 51, 53),
    53: (52, 54),
    54: (46, 53)
}

# Graph of the nodes and the adjacent edges
node_edge_graph = {
    1: (1, 7),
    2: (1, 2),
    3: (2, 3, 8),
    4: (3, 4),
    5: (4, 5, 9),
    6: (5, 6),
    7: (6, 10),
    8: (11, 19),
    9: (7, 11, 12),
    10: (12, 13, 20),
    11: (8, 13, 14),
    12: (14, 15, 21),
    13: (9, 15, 16),
    14: (16, 17, 22),
    15: (10, 17, 18),
    16: (18, 23),
    17: (24, 34),
    18: (19, 24, 25),
    19: (25, 26, 35),
    20: (20, 26, 27),
    21: (27, 28, 36),
    22: (21, 28, 29),
    23: (29, 30, 37),
    24: (22, 30, 31),
    25: (31, 32, 38),
    26: (23, 32, 33),
    27: (33, 39),
    28: (34, 40),
    29: (40, 41, 50),
    30: (35, 41, 42),
    31: (42, 43, 51),
    32: (36, 43, 44),
    33: (44, 45, 52),
    34: (37, 45, 46),
    35: (46, 47, 53),
    36: (38, 47, 48),
    37: (48, 49, 54),
    38: (39, 49),
    39: (50, 55),
    40: (55, 56, 63),
    41: (51, 56, 57),
    42: (57, 58, 64),
    43: (52, 58, 59),
    44: (59, 60, 65),
    45: (53, 60, 61),
    46: (61, 62, 66),
    47: (54, 62),
    48: (63, 67),
    49: (67, 68),
    50: (64, 68, 69),
    51: (69, 70),
    52: (65, 70, 71),
    53: (71, 72),
    54: (66, 72)
}

# Graph of the edges and the adjacent nodes
edge_node_graph = {
    1:(1, 2),
    2:(2, 3),
    3:(3, 4),
    4:(4, 5),
    5:(5, 6),
    6:(6, 7),
    7:(1, 9),
    8:(3, 11),
    9:(5, 13),
    10:(7, 15),
    11:(8, 9),
    12:(9, 10),
    13:(10, 11),
    14:(11, 12),
    15:(12, 13),
    16:(13, 14),
    17:(14, 15),
    18:(15, 16),
    19:(8, 18),
    20:(10, 20),
    21:(12, 22),
    22:(14, 24),
    23:(16, 26),
    24:(17, 18),
    25:(18, 19),
    26:(19, 20),
    27:(20, 21),
    28:(21, 22),
    29:(22, 23),
    30:(23, 24),
    31:(24, 25),
    32:(25, 26),
    33:(26, 27),
    34:(17, 28),
    35:(19, 30),
    36:(21, 32),
    37:(23, 34),
    38:(25, 36),
    39:(27, 38),
    40:(28, 29),
    41:(29, 30),
    42:(30, 31),
    43:(31, 32),
    44:(32, 33),
    45:(33, 34),
    46:(34, 35),
    47:(35, 36),
    48:(36, 37),
    49:(37, 38),
    50:(29, 39),
    51:(31, 41),
    52:(33, 43),
    53:(35, 45),
    54:(37, 47),
    55:(39, 40),
    56:(40, 41),
    57:(41, 42),
    58:(42, 43),
    59:(43, 44),
    60:(44, 45),
    61:(45, 46),
    62:(46, 47),
    63:(40, 48),
    64:(42, 50),
    65:(44, 52),
    66:(46, 54),
    67:(48, 49),
    68:(49, 50),
    69:(50, 51),
    70:(51, 52),
    71:(52, 53),
    72:(53, 54)
}

# Graph of the tiles and the adjacent nodes
tile_node_graph = {
    1: (1, 2, 3, 9, 10, 11),
    2: (3, 4, 5, 11, 12, 13),
    3: (5, 6, 7, 13, 14, 15),
    4: (8, 9, 10, 18, 19, 20),
    5: (10, 11, 12, 20, 21, 22),
    6: (12, 13, 14, 22, 23, 24),
    7: (14, 15, 16, 24, 25, 26),
    8: (17, 18, 19, 28, 29, 30),
    9: (19, 20, 21, 30, 31, 32),
    10: (21, 22, 23, 32, 33, 34),
    11: (23, 24, 25, 34, 35, 36),
    12: (25, 26, 27, 36, 37, 38),
    13: (29, 30, 31, 39, 40, 41),
    14: (31, 32, 33, 41, 42, 43),
    15: (33, 34, 35, 43, 44, 45),
    16: (35, 36, 37, 45, 46, 47),
    17: (40, 41, 42, 48, 49, 50),
    18: (42, 43, 44, 50, 51, 52),
    19: (44, 45, 46, 52, 53, 54)
}

# Graph of edges and the adjacent edges
edge_graph = {
    1: (2, 7),
    2: (1, 3, 8),
    3: (2, 4, 8),
    4: (3, 5, 9),
    5: (4, 6, 9),
    6: (5, 10),
    7: (1, 11, 12),
    8: (2, 3, 13, 14),
    9: (4, 5, 15, 16),
    10: (6, 17, 18),
    11: (7, 12, 19),
    12: (7, 11, 13, 20),
    13: (8, 12, 14, 20),
    14: (8, 13, 15, 21),
    15: (9, 14, 16, 21),
    16: (9, 15, 17, 22),
    17: (10, 16, 18, 22),
    18: (10, 17, 23),
    19: (11, 24, 25),
    20: (12, 13, 26, 27),
    21: (14, 15, 28, 29),
    22: (16, 17, 30, 31),
    23: (18, 32, 33),
    24: (19, 25, 34),
    25: (19, 24, 26, 35),
    26: (20, 25, 27, 35),
    27: (20, 26, 28, 36),
    28: (21, 27, 29, 36),
    29: (21, 28, 30, 37),
    30: (22, 29, 31, 37),
    31: (22, 30, 32, 38),
    32: (23, 31, 33, 38),
    33: (23, 32, 39),
    34: (24, 40),
    35: (25, 26, 41, 42),
    36: (27, 28, 43, 44),
    37: (29, 30, 45, 46),
    38: (31, 32, 47, 48),
    39: (33, 49),
    40: (34, 41, 50),
    41: (35, 40, 42, 50),
    42: (35, 41, 43, 51),
    43: (36, 42, 44, 51),
    44: (36, 43, 45, 52),
    45: (37, 44, 46, 52),
    46: (37, 45, 47, 53),
    47: (38, 46, 48, 53),
    48: (38, 47, 49, 54),
    49: (39, 48, 54),
    50: (40, 41, 55),
    51: (42, 43, 56, 57),
    52: (44, 45, 58, 59),
    53: (46, 47, 60, 61),
    54: (48, 49, 62),
    55: (50, 56, 63),
    56: (51, 55, 57, 63),
    57: (51, 56, 58, 64),
    58: (52, 57, 59, 64),
    59: (52, 58, 60, 65),
    60: (53, 59, 61, 65),
    61: (53, 60, 62, 66),
    62: (54, 61, 66),
    63: (55, 56, 67),
    64: (57, 58, 68, 69),
    65: (59, 60, 70, 71),
    66: (61, 62, 72),
    67: (63, 68),
    68: (64, 67, 69),
    69: (64, 68, 70),
    70: (65, 69, 71),
    71: (65, 70, 72),
    72: (66, 71)
}

# Graph of the ports and the nodes they are connected to
port_location = [
    (1, 2),
    (4, 5),
    (15, 16),
    (27, 38),
    (46, 47),
    (51, 52),
    (48, 49),
    (29, 39),
    (8, 18)
]

# port types
port_types = ["brick", "ore", "wool", "grain", "lumber", "any", "any", "any", "any"]

# tile values
tile_values = [[2, 12], [6, 6, 8, 8], 
               [3, 3, 4, 4, 5, 5, 9, 9, 10, 10, 11, 11,]]

# tile resource
tile_resource = ["brick", "brick", "brick",
            "ore", "ore", "ore",
            "wool", "wool", "wool", "wool",
            "grain", "grain", "grain", "grain",
            "lumber", "lumber", "lumber", "lumber", "desert"
            ]

"""
ADDING SOME NOTES FOR THE ACTION SPACE

Settlements: 54
Cities: 54
Roads: 72
Buy Dev Card: 1
Trade with Bank: 5
Trade with Port: 5
Use Knight: 19
Use Road Building: 2556 # might need to randomly assign this
Use Year of Plenty: 15
Use Monopoly: 5
End Turn: 1
Discard: 1
Sum: 232

ADDING NOTES FOR THE OBSERVATION SPACE

PLAYER STUFF
------------
PLAYER's NUMBER: 1
PLAYER PLAYED DEVELOPMENT CARD: 1
PLAYER RESOURCE: 5
PLAYER DEVELOPMENT CARD: 5
PLAYER LONGEST ROAD: 1
PLAYER LARGE ARMY: 1
PLAYER VICTORY POINTS: 1
PLAYER PRIVATE VICTORY POINTS: 1

BOARD STUFF
-----------
NODE SETTLEMENTS: 54
NODE CITIES: 54
EDGE ROADS: 72
PORT RESOURCE: 9
TILE RESOURCE: 19
TILE VALUE: 19
TILE ROBBER: 19

OPPONENT STUFF
--------------
OPPONENT RESOURCE: N - 1
OPPONENT DEVELOPMENT CARD: N - 1
OPPOENENT LONGEST ROAD: N - 1
OPPONENT LARGE ARMY: N - 1
OPPONENT VICTORY POINTS: N - 1

Sum: 277
"""
