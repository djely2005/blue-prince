# src/world/map.py
from typing import List, Optional, Tuple

from src.entities.inventory import Inventory
# If Adam later exposes real Room/Door types, import them here.
# For now we use a very small placeholder interface.
class Room:
    def __init__(self, name: str = "Start") -> None:
        self.name = name
        # TODO/Adem: add color, rarity, gem_cost, doors, etc.

class MoveResult:
    def __init__(self, allowed: bool, reason: str = "", candidates: Optional[List[Room]] = None) -> None:
        self.allowed = allowed
        self.reason = reason       # e.g., "MOVE_OK", "WALL", "LOCKED_NEED_KEY", "NEW_DOOR_CHOICE"
        self.candidates = candidates or []

class MansionMap:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.grid: List[List[Optional[Room]]] = [[None for _ in range(cols)] for _ in range(rows)]

    def set_room(self, pos: Tuple[int, int], room: Room) -> None:
        self.grid[pos[0]][pos[1]] = room

    def _in_bounds(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def request_move(self, cur_pos: Tuple[int, int], next_pos: Tuple[int, int], inv: Inventory) -> MoveResult:
        """
        Minimal movement rules so you can test navigation:
        - out of bounds → WALL
        - if next cell already has a room → MOVE_OK
        - if next cell unknown → NEW_DOOR_CHOICE with 3 dummy rooms (Adem will replace)
        - keys/locks will be added once Door/Room is ready.
        """
        if not self._in_bounds(next_pos):
            return MoveResult(False, "WALL")

        current_room = self.grid[cur_pos[0]][cur_pos[1]]
        if current_room is None:
            return MoveResult(False, "NO_CURRENT_ROOM")

        target_room = self.grid[next_pos[0]][next_pos[1]]
        if target_room is not None:
            # TODO: check door lock levels when Door is available
            return MoveResult(True, "MOVE_OK")

        # Unknown cell -> simulate 3 candidate rooms to choose (Adem will provide real draw)
        candidates = [Room("RedRoom"), Room("GreenRoom"), Room("BlueRoom")]
        return MoveResult(False, "NEW_DOOR_CHOICE", candidates)

