from enum import Enum

class Direction(Enum):
    TOP = (0, 1)
    BOTTOM = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    @classmethod
    def rotate(direction):
        if(direction == Direction.BOTTOM):
            return Direction.RIGHT
        if(direction == Direction.RIGHT):
            return Direction.TOP
        if(direction == Direction.TOP):
            return Direction.LEFT
        if(direction == Direction.LEFT):
            return Direction.BOTTOM
