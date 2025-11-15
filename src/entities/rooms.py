from src.entities.blue_room import BlueRoom
from src.entities.yellow_room import YellowRoom
from src.entities.violet_room import VioletRoom
from src.entities.orange_room import OrangeRoom
from src.entities.green_room import GreenRoom
from src.entities.red_room import RedRoom
from src.entities.door import Door
from src.utils.direction import Direction
from src.utils.lock_state import LockState
from src.utils.rarity import Rarity

entrance_hall = BlueRoom(
    name="Entrance Hall", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.TOP),Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.RIGHT), Door(LockState.UNLOCKED, Direction.LEFT)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/entrance_hall.png"
)

ante_chambre = BlueRoom(
    name="Antechamber", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/ante_chambre.png"
)

parlor = BlueRoom(
    name="Parlor", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/parlor.png"
)

closet = BlueRoom(
    name="Closet", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/closet.png"
)

nook = BlueRoom(
    name="Nook",
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)], 
    rarity=Rarity.COMMON,
    sprite_path="rooms/nook.png"
)

den = BlueRoom(
    name="Den",
    price=1, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.RIGHT), Door(LockState.UNLOCKED, Direction.LEFT)], 
    rarity=Rarity.COMMON, 
    sprite_path="rooms/gen.png"
)

pantry = BlueRoom(
    name="Pantry",
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)], 
    rarity=Rarity.COMMON,
    sprite_path="rooms/pantry.png"
)

laundry_room = YellowRoom(
    name="LaundryRoom",
    price=1,
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.RARE,
    sprite_path="rooms/laundry_room.png"
)

Locksmith = YellowRoom(
    name="Locksmith",
    price=1,
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.UNUSUAL,
    sprite_path="rooms/Locksmith.png"
)

bedroom = VioletRoom(
    name="BedRoom", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/bedroom.png"
)

boudoir = VioletRoom(
    name="Boudoir", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)],
    rarity=Rarity.STANDARD,
    sprite_path="rooms/boudoir.png"
)

hallway = OrangeRoom(
    name="Hallway", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT), Door(LockState.UNLOCKED, Direction.RIGHT)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/hellway.png"
)

passageway = OrangeRoom(
    name="Passageway", 
    price=2, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.TOP), Door(LockState.UNLOCKED, Direction.LEFT), Door(LockState.UNLOCKED, Direction.RIGHT)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/passegeway.png"
)

terrace = GreenRoom(
    name="Terrace", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/terrace.png"
)

veranda = GreenRoom(
    name="Veranda", 
    price=2, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.TOP)],
    rarity=Rarity.UNUSUAL,
    sprite_path="rooms/veranda.png"
)

lavatory = RedRoom(
    name="Lavatory", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)],
    rarity=Rarity.COMMON,
    sprite_path="rooms/lavatory.png"
)

gymnasium = RedRoom(
    name="Gymnasium", 
    price=0, 
    doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.RIGHT), Door(LockState.UNLOCKED, Direction.LEFT)],
    rarity=Rarity.STANDARD,
    sprite_path="rooms/gymasio.png"
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
