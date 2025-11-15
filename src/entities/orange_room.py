from src.entities.room import Room
from door import Door

from src.utils.rarity import Rarity
from src.entities.consumable_item import ConsumableItem

# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "Hallway": [
        (0.25, ConsumableItem, {'name': 'Gold', 'quantity': 1}),
        (0.15, ConsumableItem, {'name': 'Gem', 'quantity': 1})
        # the first number is for probability I just did a random number we can change it later if needed
    ],
    "Passageway": []
}

class OrangeRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, img_path: str):
        super().__init__(name, price, doors, rarity, img_path= spite, possible_items= possible_items)