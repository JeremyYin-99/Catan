from catanatron.models.player import Color
from numpy import array
from gym.spaces import MultiDiscrete

resource_str_to_num = {
    "SHEEP":1,
    "WOOD":2,
    "WHEAT":3,
    "ORE":4,
    "BRICK":5,
    "DESERT":999,
    None:0

}

# colors = [
#    Color.RED,
#    Color.BLUE,
#    Color.WHITE,
#    Color.ORANGE
# ]
p = [
    'P0','P1','P2','P3'
]


def get_observations(json_file, current_player, all_players):
    color_list = {}
    # idx = colors.index(color)
    # colors_adj = colors[idx:] + colors[:idx]
    # p_adj = p[idx:] + p[:idx]
    # print(colors_adj)
    # num = 1
    # for c in colors_adj:
    #     color_list[c.value] = num
    #     num += 1
        
    my_num = 1
    colors = []
    for i in all_players:
        colors.append(i.color)
        print(i.color.value)
        print(current_player.color.value)
        print(i.color.value == current_player.color.value)
        if i.color.value == current_player.color.value:
            data = [my_num]
        
        my_num += 1
    
    p_adj = p[my_num-1:] + p[:my_num-1]
    colors_adj = colors[my_num-1:] + colors[:my_num-1]
    
    num = 1
    for c in colors_adj:
        color_list[c.value] = num
        num += 1
        
    

    tiles = json_file['tiles']
    for tile in tiles:
        if tile['tile']['type'] == 'RESOURCE_TILE':
            data.append(resource_str_to_num[tile['tile']['resource']])
            data.append(tile['tile']['number'])
        elif tile['tile']['type'] == 'PORT':
            data.append(resource_str_to_num[tile['tile']['resource']])
        
    nodes = json_file['nodes']
    for node in range(len(nodes)):
        if nodes[node]['building'] == None:
            data.append(0)
            data.append(0)
        elif nodes[node]['building'] == 'SETTLEMENT':
            data.append(1)
            data.append(color_list[nodes[node]['color']])
        elif nodes[node]['building'] == 'CITY':
            data.append(2)
            data.append(color_list[nodes[node]['color']])
            
    edges = json_file['edges']
    for edge in edges:
        if edge['color'] == None:
            data.append(0)
        else:
            data.append(color_list[edge['color']])
            
    pla = p_adj[0]
    data.append(json_file['player_state']['{}_VICTORY_POINTS'.format(pla)])
    data.append(json_file['player_state']['{}_ROADS_AVAILABLE'.format(pla)])
    data.append(json_file['player_state']['{}_SETTLEMENTS_AVAILABLE'.format(pla)])
    data.append(json_file['player_state']['{}_CITIES_AVAILABLE'.format(pla)])
    data.append(json_file['player_state']['{}_HAS_ROAD'.format(pla)])
    data.append(json_file['player_state']['{}_HAS_ARMY'.format(pla)])
    data.append(json_file['player_state']['{}_HAS_ROLLED'.format(pla)])
    data.append(json_file['player_state']['{}_HAS_PLAYED_DEVELOPMENT_CARD_IN_TURN'.format(pla)])
    data.append(json_file['player_state']['{}_ACTUAL_VICTORY_POINTS'.format(pla)])
    data.append(json_file['player_state']['{}_LONGEST_ROAD_LENGTH'.format(pla)])
    data.append(json_file['player_state']['{}_WOOD_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_BRICK_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_SHEEP_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_WHEAT_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_ORE_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_KNIGHT_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_PLAYED_KNIGHT'.format(pla)])
    data.append(json_file['player_state']['{}_YEAR_OF_PLENTY_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_PLAYED_YEAR_OF_PLENTY'.format(pla)])
    data.append(json_file['player_state']['{}_MONOPOLY_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_PLAYED_MONOPOLY'.format(pla)])
    data.append(json_file['player_state']['{}_ROAD_BUILDING_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_PLAYED_ROAD_BUILDING'.format(pla)])
    data.append(json_file['player_state']['{}_VICTORY_POINT_IN_HAND'.format(pla)])
    data.append(json_file['player_state']['{}_PLAYED_VICTORY_POINT'.format(pla)])
    
    for pla in p_adj[1:]:
        data.append(json_file['player_state']['{}_VICTORY_POINTS'.format(pla)])
        data.append(json_file['player_state']['{}_ROADS_AVAILABLE'.format(pla)])
        data.append(json_file['player_state']['{}_SETTLEMENTS_AVAILABLE'.format(pla)])
        data.append(json_file['player_state']['{}_CITIES_AVAILABLE'.format(pla)])
        data.append(json_file['player_state']['{}_HAS_ROAD'.format(pla)])
        data.append(json_file['player_state']['{}_HAS_ARMY'.format(pla)])
        data.append(json_file['player_state']['{}_HAS_ROLLED'.format(pla)])
        data.append(json_file['player_state']['{}_HAS_PLAYED_DEVELOPMENT_CARD_IN_TURN'.format(pla)])
        data.append(json_file['player_state']['{}_ACTUAL_VICTORY_POINTS'.format(pla)])
        data.append(json_file['player_state']['{}_LONGEST_ROAD_LENGTH'.format(pla)])
        data.append(json_file['player_state']['{}_WOOD_IN_HAND'.format(pla)] + 
            json_file['player_state']['{}_BRICK_IN_HAND'.format(pla)] +
            json_file['player_state']['{}_SHEEP_IN_HAND'.format(pla)] +
            json_file['player_state']['{}_WHEAT_IN_HAND'.format(pla)] +
            json_file['player_state']['{}_ORE_IN_HAND'.format(pla)]
            )
        data.append(json_file['player_state']['{}_KNIGHT_IN_HAND'.format(pla)] +
                    json_file['player_state']['{}_YEAR_OF_PLENTY_IN_HAND'.format(pla)] +
                    json_file['player_state']['{}_MONOPOLY_IN_HAND'.format(pla)] +
                    json_file['player_state']['{}_ROAD_BUILDING_IN_HAND'.format(pla)] +
                    json_file['player_state']['{}_VICTORY_POINT_IN_HAND'.format(pla)]
                    )
        
    data.append(json_file['is_initial_build_phase'])
    data.append(json_file['robber_coordinate'][0])
    data.append(json_file['robber_coordinate'][1])
    data.append(json_file['robber_coordinate'][2])
    print(data)
    data = [int(item) for item in data]
    
    # print(data)
    
    return data
            
    
def get_state(json_file, all_players):
    color_list = {}
    colors = []
    for i in all_players:
        colors.append(i.color)
    
    colors_adj = colors
    
    num = 1
    for c in colors_adj:
        color_list[c.value] = num
        num += 1
        
    data = []
    tiles = json_file['tiles']
    for tile in tiles:
        if tile['tile']['type'] == 'RESOURCE_TILE':
            data.append(resource_str_to_num[tile['tile']['resource']])
            data.append(tile['tile']['number'])
        elif tile['tile']['type'] == 'PORT':
            data.append(resource_str_to_num[tile['tile']['resource']])
        
    nodes = json_file['nodes']
    for node in range(len(nodes)):
        if nodes[node]['building'] == None:
            data.append(0)
            data.append(0)
        elif nodes[node]['building'] == 'SETTLEMENT':
            data.append(1)
            data.append(color_list[nodes[node]['color']])
        elif nodes[node]['building'] == 'CITY':
            data.append(2)
            data.append(color_list[nodes[node]['color']])
            
    edges = json_file['edges']
    for edge in edges:
        if edge['color'] == None:
            data.append(0)
        else:
            data.append(color_list[edge['color']])
            
    # print(data)
    return data
    
        