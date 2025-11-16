from src.entities.blue_room import *
from src.entities.yellow_room import *
from src.entities.violet_room import *
from src.entities.orange_room import *
from src.entities.green_room import *
from src.entities.red_room import *

entrance_hall = EntranceHall()
entrance_hall.visited = True

ante_chambre = Antechamber()

parlor = Parlor()

closet = Closet()

nook = Nook()

den = Den()

pantry = Pantry()

commissary = Commissary()

laundry_room = LaundryRoom()

boudoir = Boudoir()

bedroom = Bedroom()

guest_bedroom = GuestBedroom()

hallway = Hallway()

terance = Terrace()

veranda = Veranda()

gymnasium = Gymnasium()

chapel = Chapel()

passageway = Passageway()
FULL_ROOM_DECK = [
    parlor,
    closet,
    nook,
    den,
    pantry,
    commissary,
    laundry_room,
    boudoir,
    bedroom,
    guest_bedroom,
    hallway,
    passageway,
    terance,
    veranda,
    gymnasium,
    chapel,
]
