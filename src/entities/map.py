from src.entities.room import Room
from src.entities.blue_room import BlueRoom
from src.utils.direction import Direction
import pygame
from src.settings import *
import math
from src.entities.rooms import ante_chambre, entrance_hall
import random
from src.entities.inventory import Inventory
from src.utils.direction import Direction

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
    def request_move(self, current_position: tuple[int, int], future_position: tuple[int, int], player: Inventory):
        # Making sure we are inside the map
        if not (future_position[0] < GRID_HEIGHT and future_position[1] < GRID_WIDTH):
            return False
        # Making sure we have a room
        if not self.__grid[current_position[0]][current_position[1]]:
            return False
        
        direction_r = future_position[0] - current_position[0]
        direction_c = future_position[1] - current_position[1]

        move_direction = None
        if direction_r == -1 and direction_c == 0 :
            move_direction = Direction.TOP
        elif direction_r == 1 and direction_c == 0 :
            move_direction = Direction.BOTTOM
        elif direction_r == 0 and direction_c == -1 :
            move_direction = Direction.LEFT
        elif direction_r == 0 and direction_c == 1 :
            move_direction = Direction.RIGHT
        else :
            return False
        
        door_to_target = None
        for door in Room.doors:
            if door.direction == move_direction:
                door_to_target = door
                break
        
        if not door_to_target:
            return False 

        return door_to_target.open_door(player)
