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
from src.entities.choice_menu import menu
_DIRECTION_MAP = {
    # AZERTY
    pygame.K_z: Direction.TOP,
    pygame.K_q: Direction.LEFT,
    pygame.K_s: Direction.BOTTOM,
    pygame.K_d: Direction.RIGHT,

    # QWERTY fallback
    pygame.K_w: Direction.TOP,
    pygame.K_a: Direction.LEFT,
}
class Map:
    def __init__(self, seed: int):
        self.__seed = seed
        self.__grid: list[Room] = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
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

    def update_selected_direction(self, player: Player, screen: pygame.Surface):
        keys = pygame.key.get_pressed()
        r, c = player.grid_position
        room: Room = self.grid[r][c]
        for key, direction in _DIRECTION_MAP.items():
            if keys[key]:

                # 1. Check if a door exists in that direction

                if not room.door_direction_exists(direction):
                    player.selected = None
                    return  # blocked, do nothing

                # 3. Update player's selection
                player.selected = direction
                # 2. Update sprite on map
                self.__update_selected_sprite(screen, player.grid_position, TILE_SIZE, player)

                return  # first key wins
        if player.selected:
            self.__update_selected_sprite(screen, player.grid_position, TILE_SIZE, player)

    def __update_selected_sprite(self, screen: pygame.Surface, pos: tuple[int, int], size: int, player: Player):
        x, y = pos
        if player.selection_sprite:
            scale_sprite = pygame.transform.scale(player.selection_sprite, (size, size))
            x = OFFSET_X + x * TILE_SIZE
            y = OFFSET_Y + y * TILE_SIZE
            if player.selected == Direction.TOP:
                scale_sprite = pygame.transform.rotate(scale_sprite, -90)
            if player.selected == Direction.BOTTOM:
                scale_sprite = pygame.transform.rotate(scale_sprite, 90)
            if player.selected == Direction.RIGHT:
                scale_sprite = pygame.transform.rotate(scale_sprite, 180)
            screen.blit(scale_sprite, (x, y))

    def draw(self, screen: pygame.Surface):
        """Draw the left-side map area."""
        map_rect = pygame.Rect(0, 0, MAP_WIDTH, HEIGHT)
        pygame.draw.rect(screen, BLUE, map_rect)

        for row_idx, row in enumerate(self.grid):
            for col_idx, room in enumerate(row):
                if isinstance(room, Room):
                    x = OFFSET_X + col_idx * TILE_SIZE
                    y = OFFSET_Y + row_idx * TILE_SIZE
                    room.draw(screen, (x, y), TILE_SIZE)
    
    def open_door(self):
        pass
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
        
    # (Dans la classe Map de map.py)

    def prepare_room_doors(self, room_template: Room, row_index: int):
        """ Modify the lock state of a room's door"""
        if room_template.name == "Entrance Hall" or room_template.name == "Antechamber":
            return room_template

        for door in room_template.doors:
            new_lock_state = self.__get_random_lockstate(row_index)
            door.lock_state = new_lock_state
        
        return room_template


map = Map(0)