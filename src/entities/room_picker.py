from src.entities.room import Room
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.utils.rarity import Rarity
from src.entities.inventory import Inventory
from src.entities.bunny_paw import BunnyPaw
import random

class RoomPicker :
    def __init__(self, rooms: list[Room], refresh_price : int, luck: BunnyPaw):
        self.__rooms = rooms
        self.__refresh_price = refresh_price
        self.__luck = luck

    @property
    def rooms(self):
        return self.__rooms
    @rooms.setter
    def rooms(self, rooms):
        self.__rooms = rooms

    @property
    def refresh_price(self):
        return self.__refresh_price
    @refresh_price.setter
    def refresh_price(self, refresh_price):
        self.__refresh_price = refresh_price

    @property
    def luck(self):
        return self.__luck
    @luck.setter
    def luck(self, luck):
        self.__luck = luck

    def weight(self, room: Room):
        weight0 = room.rarity.value
        weight = weight0 * self.__luck
        return max(1, int(weight))
    
    def generate_rooms(self, player: Inventory):
        all_rooms = list(self.__rooms)
        
        free_rooms = [r for r in all_rooms if r.price == 0]
        chosen_rooms = []
        
        if free_rooms:
            free_weight = [self.weight(r, player) for r in free_rooms]
            guaranted_free_room = random.choices(free_rooms, weights=free_weight, k=1)[0]
            chosen_rooms.append(guaranted_free_room)
            all_rooms.remove(guaranted_free_room) # To make sure we don't have the same room twice

        while len(chosen_rooms) < 3 :
            w = [self.weight(r, player) for r in all_rooms]
            chosen_room = random.choices(all_rooms, weights=w, k=1)[0]
            chosen_rooms.append(chosen_room)
            all_rooms.remove(chosen_room)
        
        return chosen_rooms