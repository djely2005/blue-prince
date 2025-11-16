from src.entities.room import Room
from src.entities.door import Door
from abc import abstractmethod
from src.entities.player import Player
from src.utils.rarity import Rarity
from src.entities.consumable_item import ConsumableItem
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.session import session

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
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, possible_items = [], img_path: str = ''):
        super().__init__(name, price, doors, rarity, session, possible_items= possible_items, img_path= img_path)
            
    @abstractmethod
    def on_enter(self, player):
        return super().on_enter(player)
    
    @abstractmethod
    def on_draft(self, player):
        return super().on_draft(player)
    
    def apply_effect(self, player: Player):
        pass


class Chapel(RedRoom):
    def __init__(self):
        name="Chapel" 
        price=0
        doors=[Door(LockState.UNLOCKED, Direction.BOTTOM)]
        rarity=Rarity.COMMON
        sprite_path="rooms/Chapel.png"
        possible_items = []
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)

    def on_enter(self, player):
        player.spend_money(1)
        return super().on_enter(player)
    
    def on_draft(self, player):
        return super().on_draft(player)

class Gymnasium(RedRoom):
    def __init__(self):
        name="Gymnasium"
        price=0
        doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.RIGHT), Door(LockState.UNLOCKED, Direction.LEFT)]
        rarity=Rarity.STANDARD
        sprite_path="rooms/Gymnasium.png"
        possible_items = [
                            (0.10, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
                            (0.05, ConsumableItem, {'name': 'Key', 'quantity': 1})
        ]
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)

    def on_enter(self, player):
        player.spend_steps(2)
    
    def on_draft(self, player):
        return super().on_draft(player)