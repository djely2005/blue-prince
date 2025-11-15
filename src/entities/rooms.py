from src.entities.blue_room import *
from src.entities.yellow_room import YellowRoom
from src.entities.violet_room import VioletRoom
from src.entities.orange_room import OrangeRoom
from src.entities.green_room import GreenRoom
from src.entities.red_room import RedRoom
from src.entities.door import Door
from src.utils.direction import Direction
from src.utils.lock_state import LockState
from src.utils.rarity import Rarity

entrance_hall = EntranceHall()

ante_chambre = Antechamber()

parlor = Parlor()

closet = Closet()

nook = Nook()

den = Den()

pantry = Pantary()

laundry_room = YellowRoom(
    name="LaundryRoom",
    price=1,
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.RARE
)

Locksmith = YellowRoom(
    name="Locksmith",
    price=1,
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.UNUSUAL
)

bedroom = VioletRoom(
    name="BedRoom", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)],
    rarity=Rarity.COMMON
)

boudoir = VioletRoom(
    name="Boudoir", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)],
    rarity=Rarity.STANDARD
)

hallway = OrangeRoom(
    name="Hallway", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT), Door(LockState.UNLOCKED, Direction.RIGHT)],
    rarity=Rarity.COMMON
)

passageway = OrangeRoom(
    name="Passageway", 
    price=2, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.TOP), Door(LockState.UNLOCKED, Direction.LEFT), Door(LockState.UNLOCKED, Direction.RIGHT)],
    rarity=Rarity.COMMON
)

terrace = GreenRoom(
    name="Terrace", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.COMMON
)

veranda = GreenRoom(
    name="Veranda", 
    price=2, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.TOP)],
    rarity=Rarity.UNUSUAL
)

lavatory = RedRoom(
    name="Lavatory", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.COMMON
)

gymnasium = RedRoom(
    name="Gymnasium", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.RIGHT), Door(LockState.UNLOCKED, Direction.LEFT)],
    rarity=Rarity.STANDARD
)

# Maybe I can use a deck for room picker not sure if I will keep it

FULL_ROOM_DECK = [
    parlor,
    closet,
    nook,
    den,
    pantry,
    laundry_room,
    Locksmith,
    bedroom,
    boudoir,
    hallway,
    passageway,
    terrace,
    veranda,
    lavatory,
    gymnasium
]
