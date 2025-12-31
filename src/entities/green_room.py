from src.entities.room import Room
from src.entities.door import Door
from abc import abstractmethod
from src.entities.player import Player
from src.utils.rarity import Rarity
from src.entities.other_item import OtherItem
from src.entities.shovel import Shovel
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.entities.consumable_item import ConsumableType
from src.entities.bunny_paw import BunnyPaw
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.session import session

# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "Terrance": [
        (0.50, OtherItem, {'name': 'Banana', 'quantity': 1}),
        (0.45, OtherItem, {'name': 'Orange', 'quantity': 1}),
        (0.40, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
        (0.35, ConsumableItem, {'name': 'Gem', 'quantity': 2}),
        (0.30, ConsumableItem, {'name': 'Gold', 'quantity': 2}),
        (0.20, Shovel, {'name': 'Shovel', 'quantity': 3})
        # the first number is for probability I just did a random number we can change it later if needed
    ],
    "Veranda": [
        (0.50, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
        (0.35, Shovel, {'name': 'Shovel', 'quantity': 1})
    ]

}

class GreenRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, possible_items = [], img_path: str = ''):
        super().__init__(name, price, doors, rarity, session, possible_items= possible_items, img_path= img_path)
    
    @abstractmethod
    def on_enter(self, player):
        return super().on_enter(player)
    
    @abstractmethod
    def on_draft(self, player):
        return super().on_draft(player)
    
    @abstractmethod
    def shop(self, player, choice: str):
        return super().shop(player)

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

class Terrace(GreenRoom):
    def __init__(self):
        name = "Terrace"
        price = 0
        doors = [Door(LockState.UNLOCKED, Direction.BOTTOM)]
        rarity = Rarity.COMMON
        sprite_path = "rooms/Terrace.png"
        possible_items =[
                            (0.50, OtherItem, {'name': 'Banana', 'quantity': 1, 'type': ConsumableType.STEP}),
                            (0.45, OtherItem, {'name': 'Orange', 'quantity': 1, 'type': ConsumableType.STEP}),
                            (0.40, ConsumableItem, {'name': 'Gem', 'quantity': 1, 'type': ConsumableType.GEM}),
                            (0.35, ConsumableItem, {'name': 'Gem', 'quantity': 2, 'type': ConsumableType.GEM}),
                            (0.30, ConsumableItem, {'name': 'Gold', 'quantity': 2, 'type': ConsumableType.MONEY}),
                            (0.20, Shovel, {}),
        ]
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)

    def on_enter(self, player):
        pass
    
    def on_draft(self, player):
        self.discover_items(player)
    
    def shop(self, player, choice: str):
        return super().shop(player, choice)

class Veranda(GreenRoom):
    def __init__(self):
        name = "Veranda"
        price = 2
        doors = [Door(LockState.UNLOCKED, Direction.BOTTOM), Door(LockState.UNLOCKED, Direction.TOP)]
        rarity = Rarity.UNUSUAL
        sprite_path = "rooms/Veranda.png"
        possible_items = [
                            (0.50, ConsumableItem, {'name': 'Gem', 'quantity': 1, 'type': ConsumableType.GEM}),
                            (0.35, Shovel, {})
        ]
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)

    def on_enter(self, player):
        pass
    
    def on_draft(self, player):
        self.discover_items(player)

    def shop(self, player, choice: str):
        return super().shop(player, choice)