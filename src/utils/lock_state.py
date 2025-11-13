from enum import Enum

class LockState(Enum):
    UNLOCKED = 0
    LOCKED = 1
    DOUBLE_LOCKED = 2

# Each value is the number of keys needed to open the door for each type
# if we have a lock_pick we can only open a locked door.