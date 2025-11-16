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
entrance_hall.visited = True

ante_chambre = Antechamber()

parlor = Parlor()

closet = Closet()

nook = Nook()

den = Den()

pantry = Pantry()


FULL_ROOM_DECK = [
    parlor,
    closet,
    nook,
    den,
    pantry
]
