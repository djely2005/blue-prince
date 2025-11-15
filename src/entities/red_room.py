from src.entities.room import Room
from src.entities.door import Door
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.consumable_item import ConsumableItem

# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "Lavatory": [],
    "Gymnasium": [
        (0.10, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
        (0.05, ConsumableItem, {'name': 'Key', 'quantity': 1})
    ]

}

class RedRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, img_path: str):
        super().__init__(name, price, doors, rarity, img_path= img_path, possible_items= possible_items)
            
    def apply_effect(self, player: Inventory):
        if self.name == "Lavatory" :
            pass 
        elif self.name == "Gymnasium":
            player.lose_steps(2)