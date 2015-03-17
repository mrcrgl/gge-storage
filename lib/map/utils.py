import math


def distance_to_castle(from_castle, to_castle):
    distance_x = from_castle.pos_x - to_castle.pos_x if from_castle.pos_x > to_castle.pos_x \
        else to_castle.pos_x - from_castle.pos_x
    distance_y = from_castle.pos_y - to_castle.pos_y if from_castle.pos_y > to_castle.pos_y \
        else to_castle.pos_y - from_castle.pos_y
    a_square = distance_x * distance_x
    b_square = distance_y * distance_y
    c_square = a_square + b_square

    return math.sqrt(c_square)