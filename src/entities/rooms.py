from src.entities.door import Door
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.entities.blue_room import BlueRoom
ante_chambre = BlueRoom(
    "Antechamber",
    0,
    [
        Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
        Door(LockState.DOUBLE_LOCKED, Direction.RIGHT),
        Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
    ]
)

entrance_hall = BlueRoom(
    "Entrance Hall",
    0,
    [
        Door(LockState.DOUBLE_LOCKED, Direction.TOP),
        Door(LockState.DOUBLE_LOCKED, Direction.RIGHT),
        Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
    ]
)
