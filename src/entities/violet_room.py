from abc import ABC, abstractmethod
from src.entities.room import Room
from src.entities.door import Door
from src.entities.object import Object
from src.utils.direction import Direction
from src.utils.lock_state import LockState
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.other_item import OtherItem
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.entities.player import Player
from src.session import session

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
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, number_of_steps: int = 1, img_path: str = '', possible_items = []):
        super().__init__(name, price, doors, rarity, session, possible_items=possible_items, img_path = img_path)
        self.number_of_steps = number_of_steps

    @abstractmethod
    def on_enter(self, player):
        return super().on_enter(player)
    
    @abstractmethod
    def on_draft(self, player):
        return super().on_draft(player)
    
    @abstractmethod
    def shop(self, player, choice: str):
        return super().shop(player, choice)

    def apply_effect(self, player: Player):
        pass


class Bedroom(VioletRoom):
    def __init__(self):
        name = "Bedroom"
        price = 0
        doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)]
        rarity=Rarity.COMMON
        sprite_path="rooms/Bedroom.webp"
        possible_items = [
                            (0.4, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
                            (0.3, OtherItem, {'name': 'Apple', 'quantity': 1}),
                            (0.2, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
                            (0.15, ConsumableItem, {'name': 'Die', 'quantity': 1}),
                            (0.15, ConsumableItem, {'name': 'Key', 'quantity': 1})
        ]
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)
    def on_draft(self, player):
        return super().on_draft(player)

    def on_enter(self, player: Player):
        player.add_steps(1)

    def shop(self, player, choice: str):
        return super().shop(player, choice)


class Boudoir(VioletRoom):
    def __init__(self):
        name = "Boudoir"
        price = 0
        doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.LEFT)]
        rarity=Rarity.STANDARD
        sprite_path="rooms/Boudoir.webp"
        possible_items = [
                            (0.25, ConsumableItem, {'name': 'Gold', 'quantity': 2}),
                            (0.20, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
                            (0.15, ConsumableItem, {'name': 'Gold', 'quantity': 5}),
                            (0.2, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
                            (0.15, ConsumableItem, {'name': 'Key', 'quantity': 1})
        ]
        super().__init__(name, price, doors, rarity, number_of_steps=2,possible_items= possible_items, img_path= sprite_path)
    def on_enter(self, player: Player):
        if not(self.visited):
            player.add_steps(2)
    
    def on_draft(self, player):
        return super().on_draft(player)
    
    def shop(self, player, choice: str):
        return super().shop(player, choice)