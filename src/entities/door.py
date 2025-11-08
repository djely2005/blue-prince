from src.utils.lock_state import LockState
from src.utils.direction import Direction

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

    