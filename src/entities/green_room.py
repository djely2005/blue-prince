from src.entities.room import Room
from src.entities.door import Door

from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.other_item import OtherItem
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem

# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "Bedroom": [
        (0.50, OtherItem, {'name': 'Banana', 'quantity': 1}),
        (0.45, OtherItem, {'name': 'Orange', 'quantity': 1}),
        (0.40, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
        (0.35, ConsumableItem, {'name': 'Gem', 'quantity': 2}),
        (0.30, ConsumableItem, {'name': 'Gold', 'quantity': 2}),
        (0.20, PermanentItem, {'name': 'Shovel', 'quantity': 3})
        # the first number is for probability I just did a random number we can change it later if needed
    ],
    "Veranda": [
        (0.50, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
        (0.35, PermanentItem, {'name': 'Shovel', 'quantity': 1})
    ]

}

class GreenRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, img_path: str):
        super().__init__(name, price, doors, rarity, img_path= spite, possible_items= possible_items)

    def apply_effect(self, player: Inventory):
        if self.name == "Terrace" :
            pass
        elif self.name == "Veranda" :
            pass