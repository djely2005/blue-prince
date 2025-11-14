from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.other_item import OtherItem
from src.entities.bunny_paw import BunnyPaw

# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "Lavatory": [],
    "Gymnasium": [
        (0.10, OtherItem, {'name': 'Gold', 'quantity': 3}),
        (0.05, OtherItem, {'name': 'Key', 'quantity': 1})
    ]

}

class RedRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity):
        super().__init__(name, price, doors, rarity, possible_items)
    
    def apply_effect(self, player: Inventory):
        if self.name == "Lavatory" :
            pass 
        elif self.name == "Gymnasium":
            player.lose_steps(2)