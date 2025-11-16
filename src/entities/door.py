from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.entities.inventory import Inventory

class Door :
    def __init__(self, lock_state: LockState, direction: Direction):
        self.__lock_state = lock_state
        self.__direction = direction
        
    @property
    def lock_state(self):
        return self.__lock_state
    @lock_state.setter
    def lock_state(self, lock_state):
        self.__lock_state = lock_state

    @property
    def direction(self):
        return self.__direction
    @direction.setter
    def direction(self, direction):
        self.__direction = direction


    # Iam not sure if this method should be added here ?
    def open_door(self, player) -> bool:
        """Attempt to open the door using the provided player's inventory.

        `player` is expected to have an `inventory` attribute exposing
        `spend_keys(n: int) -> bool`.
        """
        inv = getattr(player, "inventory", None)
        if inv is None:
            return False

        if self.__lock_state == LockState.UNLOCKED:
            return True

        if self.__lock_state == LockState.LOCKED:
            # spend a single key
            return inv.spend_keys(1)

        if self.__lock_state == LockState.DOUBLE_LOCKED:
            # need two keys
            ok1 = inv.spend_keys(1)
            if not ok1:
                return False
            ok2 = inv.spend_keys(1)
            return ok2

        return False

    