from src.entities.room import Room
from src.entities.door import Door
from src.entities.object import Object
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.other_item import OtherItem
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.entities.player import Player
import random

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
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, number_of_steps: int = 1, img_path: str = ''):
        super().__init__(name, price, doors, rarity, possible_items=possible_items, image_path = image_path)
        self.__number_of_steps = number_of_steps
    
    @property
    def number_of_steps(self):
        return self.__number_of_steps

    @number_of_steps.setter
    def number_of_steps(self, value: int):
        self.__number_of_steps = value

    def apply_effect(self, player: Player):
        if self.name == "Bedroom":
            player.add_steps(2)
        elif self.name == "Boudoir":
            player.add_steps(1) # it says it can give use few extra steps (no exact amount)


class Bedroom(VioletRoom):
    def on_enter(self, player: Player):
        player.add_steps(self.number_of_steps)


class Boudoir(VioletRoom):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, map, player: Player):
        super().__init__(name, price, doors, rarity, possible_items=possible_items)
        self.number_of_steps = map.luck_radint(1, 5, player)
    def on_enter(self, player: Player):
        player.add_steps(self.number_of_steps)