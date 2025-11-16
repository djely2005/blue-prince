from src.entities.room import Room
from src.entities.blue_room import BlueRoom
from src.entities.green_room import GreenRoom
from src.entities.pit import Pit
from src.entities.locker import Locker
from src.entities.chest import Chest
from src.entities.door import Door
from src.utils.direction import Direction
import pygame
from src.settings import *
import math
from src.entities.rooms import ante_chambre, entrance_hall, FULL_ROOM_DECK
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
        # center using integer division (0-based indices)
        start_r = GRID_HEIGHT - 1
        center_c = GRID_WIDTH // 2 + 1
        self.__grid[start_r][center_c] = entrance_hall
        self.__grid[0][center_c] = ante_chambre
        self.random = random.Random(seed)
        self.__pending_door = None  # Stores (position, direction) when door is opened
        self.__room_rotation = {}  # Tracks how many times each room is rotated
		# Game state flags
        self.game_over = False
        self.game_over_message = ""
        self.game_over_reason = None  # 'win' or 'lose'
    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value
    
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

    def draw_player_position(self, screen: pygame.Surface, player: Player):
        """Draw a small dot indicating the player's current position."""
        r, c = player.grid_position
        x = OFFSET_X + c * TILE_SIZE + TILE_SIZE // 2
        y = OFFSET_Y + r * TILE_SIZE + TILE_SIZE // 2
        # Draw a small red dot at the center of the room
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
    
    def __is_room_accessible_by_door(self, position: tuple[int, int], direction: Direction) -> bool:
        # Safely check neighbouring room and whether it has a matching door
        r, c = position
        if direction == Direction.TOP:
            nr, nc = r - 1, c
            check_dir = Direction.BOTTOM
        elif direction == Direction.BOTTOM:
            nr, nc = r + 1, c
            check_dir = Direction.TOP
        elif direction == Direction.LEFT:
            nr, nc = r, c - 1
            check_dir = Direction.RIGHT
        elif direction == Direction.RIGHT:
            nr, nc = r, c + 1
            check_dir = Direction.LEFT
        else:
            return False

        if not (0 <= nr < GRID_HEIGHT and 0 <= nc < GRID_WIDTH):
            return False

        room = self.__grid[nr][nc]
        if not isinstance(room, Room):
            return False
        return room.door_direction_exists(check_dir)

    def __insert_room(self, room: Room):
        random_door = self.random.choice(room.doors)
        # draw Room and change doors direction
        pass

    def request_move(self, current_position: tuple[int, int], future_position: tuple[int, int], player):
        # Making sure we are inside the map
        if not (0 <= future_position[0] < GRID_HEIGHT and 0 <= future_position[1] < GRID_WIDTH):
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
        
        rand_val = self.random.random()

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

    def request_place_room(self, player_pos: tuple[int, int], entry_direction: Direction, player: Player) -> list[Room]:
        """
        When a door is opened, return 3 random room choices for the player to select from.
        Room selection is influenced by player luck and current room rarity.
        This does NOT place the room yet; that happens when player selects via handle_room_selection.
        
        Args:
            player_pos: Current player position
            entry_direction: Direction of the door being opened
            player: Player object (for luck stat)
        
        Returns:
            List of 3 Room objects to choose from
        """
        # Store the door info for later placement
        self.__pending_door = (player_pos, entry_direction)
        
        # Get current room to determine rarity context
        current_room = self.__grid[player_pos[0]][player_pos[1]]
        current_rarity = current_room.rarity.value if isinstance(current_room, Room) else 0
        
        # Use player luck to weight room selection
        # Higher luck = better (higher rarity) rooms more likely
        luck_multiplier = player.luck
        
        # Create weighted room choices based on rarity and luck
        weighted_choices = []
        for room in FULL_ROOM_DECK:
            room_rarity = room.rarity.value
            
            # Calculate weight: higher luck increases chance of rarer rooms
            # Formula: base_weight * (1 + luck_bonus * relative_rarity)
            rarity_bonus = max(0, room_rarity - current_rarity) * luck_multiplier
            base_weight = 1.0
            final_weight = base_weight + rarity_bonus
            
            weighted_choices.append((room, final_weight))
        
        # Normalize weights to probabilities
        total_weight = sum(w for _, w in weighted_choices)
        probabilities = [w / total_weight for _, w in weighted_choices]
        rooms = [r for r, _ in weighted_choices]
        
        # Use the map's seeded random to select 3 rooms based on weights
        # Sample without replacement, using weights
        selected = []
        remaining_rooms = list(rooms)
        remaining_probs = list(probabilities)
        
        for _ in range(min(3, len(rooms))):
            if not remaining_rooms:
                break
            
            # Normalize remaining probabilities
            total = sum(remaining_probs)
            normalized = [p / total for p in remaining_probs]
            
            # Use seeded random to pick one room
            idx = self.random.choices(range(len(remaining_rooms)), weights=normalized, k=1)[0]
            selected.append(remaining_rooms[idx])
            
            # Remove selected room from remaining
            remaining_rooms.pop(idx)
            remaining_probs.pop(idx)
        
        return selected

    def reset(self, seed: int):
        """Reset the map to a fresh state using `seed` for deterministic RNG.
        This mirrors the initialization logic so callers can reuse the module-level
        `game_map` instance without re-importing modules.
        """
        self.__seed = seed
        self.__grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        start_r = GRID_HEIGHT - 1
        center_c = GRID_WIDTH // 2 + 1
        # reuse templates from rooms module
        self.__grid[start_r][center_c] = entrance_hall
        self.__grid[0][center_c] = ante_chambre
        self.random = random.Random(seed)
        self.__pending_door = None
        self.__room_rotation = {}
        self.game_over = False
        self.game_over_message = ""
        self.game_over_reason = None

    def handle_room_selection(self, selected_room: Room, player: Player) -> bool:
        """
        Place the selected room on the map and move the player into it.
        
        Args:
            selected_room: The room the player selected
            player: The player object
            
        Returns:
            True if room was placed successfully, False otherwise
        """
        if not self.__pending_door:
            return False

        player_pos, entry_direction = self.__pending_door
        r, c = player_pos

        # Calculate the new room position based on the direction
        if entry_direction == Direction.TOP:
            new_r, new_c = r - 1, c
        elif entry_direction == Direction.BOTTOM:
            new_r, new_c = r + 1, c
        elif entry_direction == Direction.LEFT:
            new_r, new_c = r, c - 1
        elif entry_direction == Direction.RIGHT:
            new_r, new_c = r, c + 1
        else:
            return False

        # Check bounds
        if not (0 <= new_r < GRID_HEIGHT and 0 <= new_c < GRID_WIDTH):
            return False

        # Check if position is already occupied
        if self.__grid[new_r][new_c] is not None:
            return False

        # Create a shallow clone of the room with new Door instances
        # (deepcopy fails because pygame.Surface objects can't be pickled)
        new_room = self._clone_room(selected_room)

        # Rotate the room so its doors match the entry direction
        # The entry door should be opposite to entry_direction
        opposite_dir = self._get_opposite_direction(entry_direction)
        rotations = self._calculate_rotations(new_room, opposite_dir)

        for _ in range(rotations):
            self._rotate_room_doors(new_room)

        # Record visual rotation on the room so its sprite is drawn in the same orientation
        prev_rot = getattr(new_room, '_Room__rotation', 0)
        new_room._Room__rotation = (prev_rot + rotations) % 4

        # Determine lock states for the placed room's doors according to rules:
        # - Entrance level (level 0) and level 1 (row above entrance) => UNLOCKED
        # - Antechamber (topmost level) => DOUBLE_LOCKED
        # - Other rooms: random, influenced by player.luck and the level
        max_level = GRID_HEIGHT - 1
        # level 0 corresponds to the entrance row (bottom). Compute level from new_r.
        level = (GRID_HEIGHT - 1) - new_r

        for door in new_room.doors:
            # Entrance and adjacent rows unlocked
            if level in (0, 1):
                door.lock_state = LockState.UNLOCKED
                continue

            # Antechamber (topmost level) double locked
            if level == max_level:
                door.lock_state = LockState.DOUBLE_LOCKED
                continue

            # For other levels, determine probabilities based on level and player luck.
            # Higher level -> higher chance of stronger locks. Higher luck -> lower chance.
            rng = self.random.random()
            # base factors
            level_factor = level / max_level  # 0..1
            luck_factor = max(1.0, getattr(player, 'luck', 1.0))

            # compute thresholds (clamped)
            double_thresh = min(0.85, (0.35 + 0.45 * level_factor) / luck_factor)
            locked_thresh = min(0.95, double_thresh + (0.25 + 0.35 * level_factor) / luck_factor)

            if rng < double_thresh:
                door.lock_state = LockState.DOUBLE_LOCKED
            elif rng < locked_thresh:
                door.lock_state = LockState.LOCKED
            else:
                door.lock_state = LockState.UNLOCKED

        # Check if player can afford the room
        if new_room.price > player.inventory.gems.quantity:
            return False

        # Deduct the cost
        player.inventory.spend_gems(new_room.price)

        # Place the room on the map
        self.__grid[new_r][new_c] = new_room

        # Move the player to the new room
        player.grid_position = (new_r, new_c)

        # Trigger on_enter effect
        # Provide the map's seeded RNG to the room so room effects (shops) can be deterministic
        setattr(new_room, '_room_random', self.random)
        # Attach an event to the room automatically depending on its type.
        # Use the map's seeded RNG so event placement is deterministic.
        try:
            rnd = self.random
            # Green rooms -> Pit; Blue rooms -> Locker; Others -> Chest (lower chance)
            if isinstance(selected_room, GreenRoom):
                if rnd.random() < 0.35:
                    evt = Pit()
                    setattr(evt, '_room_random', rnd)
                    new_room.event = evt
            elif isinstance(selected_room, BlueRoom):
                if rnd.random() < 0.35:
                    evt = Locker()
                    setattr(evt, '_room_random', rnd)
                    new_room.event = evt
            else:
                # Other rooms (red/orange/etc) get chests less frequently
                if rnd.random() < 0.25:
                    evt = Chest()
                    setattr(evt, '_room_random', rnd)
                    new_room.event = evt
        except Exception:
            # non-fatal: if event classes aren't available, skip event spawning
            pass

        new_room.on_draft(player)
        new_room.on_enter(player)

        # If this room is the Antechamber, the player wins the game
        try:
            if getattr(new_room, 'name', '') == 'Antechamber':
                self.game_over = True
                self.game_over_message = 'You reached the Antechamber — You win!'
                self.game_over_reason = 'win'
        except Exception:
            pass

        # Synchronize adjacent room doors
        self._synchronize_adjacent_doors(new_r, new_c)

        # Clear pending door
        self.__pending_door = None

        return True

    def _get_opposite_direction(self, direction: Direction) -> Direction:
        """Get the opposite direction."""
        if direction == Direction.TOP:
            return Direction.BOTTOM
        elif direction == Direction.BOTTOM:
            return Direction.TOP
        elif direction == Direction.LEFT:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.LEFT
        return direction

    def _calculate_rotations(self, room: Room, target_direction: Direction) -> int:
        """
        Calculate how many 90° rotations are needed to align a door to target_direction.
        Returns number of rotations (0-3).
        """
        # Find if room has a door in the target direction
        rotations = 0
        for _ in range(4):
            if room.door_direction_exists(target_direction):
                return rotations
            # Rotate 90° clockwise
            rotations += 1
            for door in room.doors:
                door.direction = Direction.rotate(door.direction)

        # If no door found in any rotation, return 0
        return 0

    def _rotate_room_doors(self, room: Room):
        """Rotate all room doors 90° clockwise."""
        for door in room.doors:
            door.direction = Direction.rotate(door.direction)

    def _clone_room(self, room: Room) -> Room:
        """
        Create a shallow clone of a room with new Door instances.
        This avoids issues with deepcopy and pygame.Surface objects.
        """
        # Create a new room of the same type with the same properties
        cloned_doors = []
        for door in room.doors:
            # Create a new Door with the same lock_state and direction
            new_door = Door(door.lock_state, door.direction)
            cloned_doors.append(new_door)

        # Create a new room instance with cloned doors
        # We use the constructor to recreate the room
        cloned_room = room.__class__.__new__(room.__class__)
        
        # Copy attributes manually (avoiding pygame.Surface deepcopy)
        cloned_room._Room__name = room.name
        cloned_room._Room__price = room.price
        cloned_room._Room__doors = cloned_doors
        cloned_room._Room__rarity = room.rarity
        cloned_room._Room__possible_items = room.possible_items
        cloned_room._Room__available_items = list(room.available_items) if room.available_items else []
        cloned_room._Room__sprite = room._Room__sprite  # Share sprite (it's read-only)
        cloned_room._Room__visited = False  # Reset visited state
        cloned_room.session = room.session

        return cloned_room

    def _synchronize_adjacent_doors(self, r: int, c: int):
        """
        Ensure that if a door on one side of a room is unlocked,
        the opposite door on the adjacent room is also unlocked.
        """
        current_room = self.__grid[r][c]
        if not isinstance(current_room, Room):
            return

        # Check each direction and synchronize with adjacent rooms
        directions = [
            (Direction.TOP, r - 1, c, Direction.BOTTOM),
            (Direction.BOTTOM, r + 1, c, Direction.TOP),
            (Direction.LEFT, r, c - 1, Direction.RIGHT),
            (Direction.RIGHT, r, c + 1, Direction.LEFT),
        ]

        for current_dir, adj_r, adj_c, opposite_dir in directions:
            # Check bounds
            if not (0 <= adj_r < GRID_HEIGHT and 0 <= adj_c < GRID_WIDTH):
                continue

            adjacent_room = self.__grid[adj_r][adj_c]
            if not isinstance(adjacent_room, Room):
                continue

            # Find the door in the current room facing this direction
            current_door = None
            for door in current_room.doors:
                if door.direction == current_dir:
                    current_door = door
                    break

            # Find the door in the adjacent room facing the opposite direction
            adjacent_door = None
            for door in adjacent_room.doors:
                if door.direction == opposite_dir:
                    adjacent_door = door
                    break

            # Synchronize: if either door is UNLOCKED, make both UNLOCKED
            if current_door and adjacent_door:
                if current_door.lock_state == LockState.UNLOCKED or adjacent_door.lock_state == LockState.UNLOCKED:
                    current_door.lock_state = LockState.UNLOCKED
                    adjacent_door.lock_state = LockState.UNLOCKED

    def get_adjacent_visited_rooms(self, player_pos: tuple[int, int]) -> dict:
        """
        Get all visited rooms adjacent to the player's current position.
        
        Returns:
            Dictionary mapping Direction -> Room for each visited adjacent room
        """
        r, c = player_pos
        adjacent_visited = {}

        directions = [
            (Direction.TOP, r - 1, c),
            (Direction.BOTTOM, r + 1, c),
            (Direction.LEFT, r, c - 1),
            (Direction.RIGHT, r, c + 1),
        ]

        for direction, adj_r, adj_c in directions:
            # Check bounds
            if not (0 <= adj_r < GRID_HEIGHT and 0 <= adj_c < GRID_WIDTH):
                continue
            adjacent_room = self.__grid[adj_r][adj_c]
            # Include the room if it exists and has been visited
            if isinstance(adjacent_room, Room):
                adjacent_visited[direction] = adjacent_room
        return adjacent_visited


    def check_if_room_exist_in_position(self, player: Player, target_direction: Direction):
        r, c = player.grid_position

        # Calculate target position
        if target_direction == Direction.TOP:
            new_r, new_c = r - 1, c
        elif target_direction == Direction.BOTTOM:
            new_r, new_c = r + 1, c
        elif target_direction == Direction.LEFT:
            new_r, new_c = r, c - 1
        elif target_direction == Direction.RIGHT:
            new_r, new_c = r, c + 1
        else:
            return False

        # Check bounds
        if not (0 <= new_r < GRID_HEIGHT and 0 <= new_c < GRID_WIDTH):
            return False

        target_room = self.__grid[new_r][new_c]
        
        # Must be a visited room
        if not isinstance(target_room, Room):
            return False
        return True
    def move_to_adjacent_room(self, player: Player, target_direction: Direction) -> bool:
        """
        Move the player to an adjacent visited room.
        
        Args:
            player: The player object
            target_direction: The direction to move (TOP, BOTTOM, LEFT, RIGHT)
            
        Returns:
            True if move was successful, False otherwise
        """
        r, c = player.grid_position

        # Calculate target position
        if target_direction == Direction.TOP:
            new_r, new_c = r - 1, c
        elif target_direction == Direction.BOTTOM:
            new_r, new_c = r + 1, c
        elif target_direction == Direction.LEFT:
            new_r, new_c = r, c - 1
        elif target_direction == Direction.RIGHT:
            new_r, new_c = r, c + 1
        else:
            return False

        # Check bounds
        if not (0 <= new_r < GRID_HEIGHT and 0 <= new_c < GRID_WIDTH):
            return False

        target_room = self.__grid[new_r][new_c]
        
        # Must be a visited room
        if not isinstance(target_room, Room):
            return False

        # Move the player
        player.grid_position = (new_r, new_c)
        target_room.on_enter(player)
        player.spend_steps(1)
        return True


game_map = Map(50)