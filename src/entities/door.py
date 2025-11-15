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
    def open_door(self, player: Inventory) -> bool:
        """Open the door with the keys of the player's inventory"""  
        if self.__lock_state == LockState.UNLOCKED:
            return True
            
        elif self.__lock_state == LockState.LOCKED:
            if player.can_open_level1_for_free():
                return True
            return player.try_spend_key()
            
        elif self.__lock_state == LockState.DOUBLE_LOCKED:
            player.try_spend_key()
            return player.try_spend_key() # 2 keys
            
        return False

    