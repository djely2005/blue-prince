from src.entities.room import Room
from src.entities.blue_room import BlueRoom
from src.utils.direction import Direction
import pygame
from src.settings import *
import math
from src.entities.rooms import ante_chambre, entrance_hall
import random
from src.entities.inventory import Inventory
from src.utils.lock_state import LockState
from src.entities.player import Player

class Map:
    def __init__(self, seed: int):
        self.__seed = seed
        self.__grid: list[Room] = [[entrance_hall for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.__grid[math.ceil(GRID_HEIGHT/2)][math.ceil(GRID_WIDTH/2)] = entrance_hall
        self.__grid[0][math.ceil(GRID_WIDTH/2)] = ante_chambre
        self.random = random.Random(seed)
        

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
        current_room = self.__grid[current_position[0]][current_position[1]]
        if not current_room:
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
        for door in current_room.doors:
            if door.direction == move_direction:
                door_to_target = door
                break
        
        if not door_to_target:
            return False 

        return door_to_target.open_door(player)

    def __get_random_lockstate(self, row_index: int) -> LockState:
        """Find the lock state of a door based on the row_index of map"""
        start_row = math.ceil(GRID_HEIGHT / 2)
        end_row = 0                         

        if row_index == start_row: # level 0
            return LockState.UNLOCKED

        if row_index == end_row: # the last level
            return LockState.DOUBLE_LOCKED

        total_distance = start_row - end_row
        current_distance = start_row - row_index
        progress = current_distance / total_distance
        
        rand_val = random.random()

        if rand_val < (progress * 0.5): # 50% chances to have a DOUBLE_LOCKED
            return LockState.DOUBLE_LOCKED
        elif rand_val < (progress * 0.8): # 80% chances to have a LOCKED
            return LockState.LOCKED
        else: # 30% chances to have an UNLOCKED
            return LockState.UNLOCKED

    def prepare_room_doors(self, room_template: Room, row_index: int):
        """ Modify the lock state of a room's door"""
        if room_template.name == "Entrance Hall" or room_template.name == "Antechamber":
            return room_template

        for door in room_template.doors:
            new_lock_state = self.__get_random_lockstate(row_index)
            door.lock_state = new_lock_state
        
        return room_template
    
    def rotate_room(self, room: Room, rotations: int):
        """Rotate a room following a clockwise direction (sens des aiguilles d'une montre)"""
        for _ in range(rotations):
            for door in room.doors:
                if door.direction == Direction.TOP:
                    door.direction = Direction.RIGHT
                elif door.direction == Direction.RIGHT:
                    door.direction = Direction.BOTTOM
                elif door.direction == Direction.BOTTOM:
                    door.direction = Direction.LEFT
                elif door.direction == Direction.LEFT:
                    door.direction = Direction.TOP

        return room
    
    def align_room(self, room: Room, needed_direction: Direction):
        """Rotate room so that one door matches the needed direction"""
        for _ in range(4):
            if any(door.direction == needed_direction for door in room.doors):
                return room
            self.rotate_room(room, 1)

        return room