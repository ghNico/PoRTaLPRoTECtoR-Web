import numpy as np

MAP_OBSTACLE_VALUE = 5


def create_movement(PATH, enemys):
    """
    Generate all positions and rotation states of enemys based on their velocity while travelling along the path from start to end.

    Arguments: global path of the map, list of all enemys for the current wave

    Test:
        -care that the velocity can not be zero, check for the values in the list of enemys
        -check that the path and enemys are given

    Raises: IndexError is reached at the endpoint of path
    """
    for e in enemys:
        enemy_movement = []
        for k in range(len(PATH)):
            for i in range(0, round(100 / e.velocity)):
                try:
                    diffposx = PATH[k + 1][1] - PATH[k][1]
                    diffposy = PATH[k + 1][2] - PATH[k][2]
                    direction = enemy_rotation(PATH[k+1][0])
                except IndexError:
                    break
                enemy_movement.append((diffposx * (i / round(100 / e.velocity)) + PATH[k][1],
                                       diffposy * (i / round(100 / e.velocity)) + PATH[k][2], direction))
        e.path = enemy_movement

def enemy_rotation(current_pos):
    """
    Translate rotation state of a given position into value

    Arguments: position

    Test:
        -check if the position is in the format needed for conversion
        -error handling when no current position

    """
    if current_pos == 'up':
        return 1
    elif current_pos == 'down':
        return 3
    elif current_pos == 'right':
        return 0
    elif current_pos == 'left':
        return 2


def build_path(way, map, pos_x, pos_y):
    """
    Recursive function to build the path of a given map

    Arguments: empty way, map, start position

    Test:
        -check if there is an end to go to
        -check if the map is in the 6x13 format

    Returns: path with all rotation states

    """
    map[pos_y, pos_x] = 0
    if pos_x < 7 and map[pos_y, pos_x + 1] == 8:
        way.append(("right", pos_x + 1, pos_y))
        build_path(way, map, pos_x + 1, pos_y)
    elif pos_x > 0 and map[pos_y, pos_x - 1] == 8:
        way.append(("left", pos_x - 1, pos_y))
        build_path(way, map, pos_x - 1, pos_y)
    elif pos_y > 0 and map[pos_y - 1, pos_x] == 8:
        way.append(("up", pos_x, pos_y - 1))
        build_path(way, map, pos_x, pos_y - 1)
    elif pos_y < 7 and map[pos_y + 1, pos_x] == 8:
        way.append(("down", pos_x, pos_y + 1))
        build_path(way, map, pos_x, pos_y + 1)
    elif pos_x < 7 and map[pos_y, pos_x + 1] == 2:
        way.append(("right", pos_x + 1, pos_y))
    elif pos_x > 0 and map[pos_y, pos_x - 1] == 2:
        way.append(("left", pos_x - 1, pos_y))
    elif pos_y > 0 and map[pos_y - 1, pos_x] == 2:
        way.append(("up", pos_x, pos_y - 1))
    elif pos_y < 7 and map[pos_y + 1, pos_x] == 2:
        way.append(("down", pos_x, pos_y + 1))
    return way


def distance_to_path(map, pos_x, pos_y):
    """
    Checker function for distance of a position on map to the next way needed for obstacle generation

    Arguments:  map, position

    Test:
        -no check needed for a position on the way but it would give 1 as distance, lack of return 0
        -check if the map is in the 6x13 format

    Returns: distance from 1 to 4 to the next way

    """
    if pos_x < 7 and map[pos_y, pos_x + 1] == 8 or pos_x > 0 and map[pos_y, pos_x - 1] == 8 or pos_y > 0 and map[
        pos_y - 1, pos_x] == 8 or pos_y < 7 and map[pos_y + 1, pos_x] == 8:
        return 1
    elif pos_x < 6 and map[pos_y, pos_x + 2] == 8 or pos_x > 0 and map[pos_y, pos_x - 2] == 8 or pos_y > 0 and map[
        pos_y - 2, pos_x] == 8 or pos_y < 6 and map[pos_y + 2, pos_x] == 8:
        return 2
    elif pos_x < 5 and map[pos_y, pos_x + 3] == 8 or pos_x > 0 and map[pos_y, pos_x - 3] == 8 or pos_y > 0 and map[
        pos_y - 3, pos_x] == 8 or pos_y < 5 and map[pos_y + 3, pos_x] == 8:
        return 3
    else:
        return 4


def generate_obstacles(map):
    """
    Random obstacle generation of the map

    Arguments: map

    Test:
        -the distance_to_path function needs to deliver exactly values from 1 to 4
        -check if the map is in the 6x13 format

    Returns: map with random obstacles

    Notes: Probability of obstacle generation is increased with distance to path
    """
    k = map
    sum_obstacles = 0
    while sum_obstacles < 8:
        for y in range(8):
            for x in range(8):
                if k[y, x] == 0:
                    distance = distance_to_path(map, x, y)
                    value = np.random.randint(0, 100)
                    if distance == 1 and value < 5 or distance == 2 and value < 20 or distance == 3 and value < 50 or distance == 4:
                        k[y, x] = MAP_OBSTACLE_VALUE
                        sum_obstacles += 1
    return k