from enum import Enum

class LockState(Enum):
    UNLOCKED = 1
    LOCKED = 2
    DOUBLE_LOCKED = 3