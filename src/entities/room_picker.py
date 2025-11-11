from room import Room
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.utils.rarity import Rarity
from src.entities.inventory import Inventory
import random

class RoomPicker :
    def __init__(self, rooms: list[Room], refresh_price : int):
        self.__rooms = rooms
        self.__refresh_price = refresh_price

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

    def drop_rate(self, room: Room, player: Inventory):
        drop_rate0 = room.rarity.value
        luck_player = 1.0
        if Inventory.has_bunny_paw:
            luck_player = 1.5
        drop_rate = drop_rate0 * luck_player
        return max(1, int(drop_rate))
    
    def generate_rooms(self, player_inventory: Inventory):
        all_rooms = list(self.__rooms)
        
        free_rooms = [r for r in all_rooms if r.price == 0]
        chosen_rooms = []
        
        if free_rooms:
            free_dr = [self.drop_rate(r, player_inventory) for r in free_rooms]
            guaranted_free_room = random.choices(free_rooms, weights=free_dr, k=1)[0]
            chosen_rooms.append(guaranted_free_room)
            all_rooms.remove(guaranted_free_room) # To make we don't have the same room twice