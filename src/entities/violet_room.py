from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.other_item import OtherItem
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem

# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "Bedroom": [
        (0.4, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
        (0.3, OtherItem, {'name': 'Apple', 'quantity': 1}),
        (0.2, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
        (0.15, ConsumableItem, {'name': 'Die', 'quantity': 1}),
        (0.15, ConsumableItem, {'name': 'Key', 'quantity': 1})
        # the first number is for probability I just did a random number we can change it later if needed
    ],
    "Boudoir": [
        (0.25, ConsumableItem, {'name': 'Gold', 'quantity': 2}),
        (0.20, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
        (0.15, ConsumableItem, {'name': 'Gold', 'quantity': 5}),
        (0.2, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
        (0.15, ConsumableItem, {'name': 'Key', 'quantity': 1})
    ]

}

class VioletRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, img_path: str):
        super().__init__(name, price, doors, rarity, img_path= spite, possible_items= possible_items)
            
    def apply_effect(self, player: Inventory):
        if self.name == "Bedroom":
            player.add_steps(2)
        elif self.name == "Boudoir":
            player.add_steps(1) # it says it can give use few extra steps (no exact amount)
    