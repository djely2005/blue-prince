from src.entities.room import Room
from src.entities.door import Door
from abc import abstractmethod
from src.entities.player import Player
from src.utils.rarity import Rarity
from src.entities.consumable_item import ConsumableItem
from src.entities.consumable_item import ConsumableType
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.session import session

# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "Lavatory": [],
    "Gymnasium": [
        (0.10, ConsumableItem, {'name': 'Gold', 'quantity': 3, 'type': ConsumableType.MONEY}),
        (0.05, ConsumableItem, {'name': 'Key', 'quantity': 1, 'type': ConsumableType.KEY})
    ]

}

class RedRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, possible_items = [], img_path: str = ''):
        super().__init__(name, price, doors, rarity, session, possible_items= possible_items, img_path= img_path)
        self.possible_items = possible_items
    @abstractmethod
    def on_enter(self, player):
        return super().on_enter(player)
    
    @abstractmethod
    def on_draft(self, player):
        return super().on_draft(player)

    def apply_effect(self, player: Player):
        pass
    
    def discover_items(self, player):
        """
        Samples items from possible_items based on player luck.
        Luck increases probability of discovering items (minimum 10%).
        """
        for probability, item_class, kwargs in self.possible_items:
            # Adjust probability by player luck (multiplier between 0.1 and 1.0)
            final_prob = probability * max(0.1, player.luck)
            if self._room_random.random() < final_prob:
                # Create the item and add to inventory
                item = item_class(**kwargs)
                if hasattr(item, 'type') and hasattr(item.type, 'name'):
                    # ConsumableItem: add to otherItems
                    self.available_items.append(item)
                else:
                    # PermanentItem or OtherItem: add accordingly
                    self.available_items.append(item)


class Chapel(RedRoom):
    def __init__(self):
        name="Chapel" 
        price=0
        doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.RIGHT), Door(LockState.UNLOCKED, Direction.LEFT)]
        rarity=Rarity.COMMON
        sprite_path="rooms/Chapel.png"
        possible_items = []
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)
    def on_enter(self, player):
        player.spend_money(1)
        return super().on_enter(player)
    
    def on_draft(self, player):
        self.discover_items(player)

class Gymnasium(RedRoom):
    def __init__(self):
        name="Gymnasium"
        price=0
        doors=[Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.RIGHT), Door(LockState.UNLOCKED, Direction.LEFT)]
        rarity=Rarity.STANDARD
        sprite_path="rooms/Gymnasium.png"
        possible_items = [
            (0.10, ConsumableItem, {'name': 'Gold', 'quantity': 3, 'type': ConsumableType.MONEY}),
            (0.05, ConsumableItem, {'name': 'Key', 'quantity': 1, 'type': ConsumableType.KEY})
        ]
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)

    def on_enter(self, player):
        player.spend_steps(2)
        return super().on_enter(player)
    
    def on_draft(self, player):
        self.discover_items(player)