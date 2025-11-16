from src.entities.blue_room import *
from src.entities.yellow_room import LaundryRoom, Locksmith
from src.entities.violet_room import Bedroom, Boudoir
from src.entities.orange_room import Hallway, Passageway
from src.entities.green_room import Veranda, Terrace
from src.entities.red_room import Gymnasium, Lavatory

entrance_hall = EntranceHall()

ante_chambre = Antechamber()

parlor = Parlor()

closet = Closet()

nook = Nook()

den = Den()

pantry = Pantary()

laundry_room = LaundryRoom()

locksmith = Locksmith()

bedroom = Bedroom()

boudoir = Boudoir()

hallway = Hallway()

passageway = Passageway()

terrace = Terrace()

veranda = Veranda()

lavatory = Lavatory()

gymnasium = Gymnasium()

# Maybe I can use a deck for room picker 

FULL_ROOM_DECK = [
    parlor,
    closet,
    nook,
    den,
    pantry,
    laundry_room,
    locksmith,
    bedroom,
    boudoir,
    hallway,
    passageway,
    terrace,
    veranda,
    lavatory,
    gymnasium
]