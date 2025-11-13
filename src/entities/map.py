from src.entities.room import Room
from src.entities.blue_room import BlueRoom
from src.utils.direction import Direction
import pygame
from src.settings import *
import math
from src.entities.rooms import ante_chambre, entrance_hall
import random

class Map:
    def __init__(self, seed: int):
        self.__seed = seed
        self.__grid: list[Room] = [[entrance_hall for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.__grid[math.ceil(GRID_HEIGHT/2)][math.ceil(GRID_WIDTH/2)] = entrance_hall
        self.__grid[0][math.ceil(GRID_WIDTH/2)] = ante_chambre
        random.seed(seed)
        
        
    
    @property
    def seed(self, seed):
        self.__seed = seed

    @seed.setter
    def seed(self):
        return self.__seed
    
    @property
    def grid(self):
        return self.__grid

    def draw(self, screen: pygame.Surface):
        """Draw the left-side map area."""
        map_rect = pygame.Rect(0, 0, MAP_WIDTH, HEIGHT)
        TILE_SIZE = 64
        OFFSET_X = 20
        OFFSET_Y = 20
        pygame.draw.rect(screen, BLUE, map_rect)

        for row_idx, row in enumerate(self.grid):
            for col_idx, room in enumerate(row):
                if isinstance(room, Room):
                    x = OFFSET_X + col_idx * TILE_SIZE
                    y = OFFSET_Y + row_idx * TILE_SIZE
                    room.draw(screen, (x, y), TILE_SIZE)

    def __is_room_accessible_by_door(self, position: tuple[int, int], direction: Direction) -> bool:
        try:
            room: Room 
            match direction:
                case Direction.TOP:
                    room = self.grid(position[0], position[1] - 1)
                    return room.door_direction_exists(Direction.BOTTOM)
                case Direction.BOTTOM:
                    room = self.grid(position[0], position[1] + 1)
                    return room.door_direction_exists(Direction.TOP)
                case Direction.LEFT:
                    room = self.grid(position[0] - 1, position[1])
                    return room.door_direction_exists(Direction.RIGHT)

                case Direction.RIGHT:
                    room = self.grid(position[0] + 1, position[1])
                    return room.door_direction_exists(Direction.LEFT)
        except IndexError:
            print('It hit the limit of the map')
            return False

    def __insert_room(self, room: Room):
        random_door = random.choice(room.doors)
        # draw Room and change doors direction
        pass