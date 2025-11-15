# Blueprint
from src.entities.room import Room
from door import Door

from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.other_item import OtherItem
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.entities.bunny_paw import BunnyPaw

# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "Parlor": [
        (0.30, OtherItem, {'name': 'Appel', 'quantity': 1})
        # the first number is for probability I just did a random number we can change it later if needed
    ],
    "Closet": [
        (0.35, ConsumableItem, {'name': 'Die', 'quantity': 1}),
        (0.30, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
        (0.25, ConsumableItem, {'name': 'Key', 'quantity': 1}),
        (0.20, PermanentItem, {'name': 'Metal Detector', 'quantity': 1}),
        (0.15, PermanentItem, {'name': 'Shovel', 'quantity': 1}),
        (0.05, BunnyPaw, {'name': 'BunnyPaw', 'quantity': 1})
    ],
    "Nook": [
        (0.30, ConsumableItem, {'name': 'Die', 'quantity': 1})
    ],
    "Den": [
        (0.30, ConsumableItem, {'name': 'Die', 'quantity': 1}),
        (0.05, BunnyPaw, {'name': 'BunnyPaw', 'quantity': 1})
    ],
    "Pantry": [
        (0.35, OtherItem, {'name': 'Appel', 'quantity': 1}),
        (0.25, OtherItem, {'name': 'Appel', 'quantity': 3}),
        (0.20, OtherItem, {'name': 'Banana', 'quantity': 1}),
        (0.15, OtherItem, {'name': 'Banana', 'quantity': 2}),
        (0.15, OtherItem, {'name': 'Orange', 'quantity': 1})
    ]

}

class BlueRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, img_path: str):
        super().__init__(name, price, doors, rarity, img_path= spite, possible_items= possible_items)
    
    def apply_effect(self, player: Inventory):
        if self.name == "Nook":
            player.add_keys(1)
        elif self.name == "Den":
            player.add_gems(1)
        elif self.name == "Pantry":
            player.add_gold(4)
        elif self.name == "Antechamber":
            print("You Win") # Maybe we can add a fon win in game to restart the game or insert a funny photo 
    
    def draft_effect(self, player):
        pass
    