from enum import Enum
from random import randint as rand

class Directions(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def randobool(r, mxr):
    t = rand(0, mxr)
    return (t <= r)


def randcell(w,h):
    tw = rand(0, w - 1)
    th = rand(0, h - 1)
    return (th, tw)

def randNeigbor(x, y):
    t = rand(0, len(Directions) - 1)
    dx, dy = MOVES[t][0], MOVES[t][1]
    return(x + dx, y + dy)