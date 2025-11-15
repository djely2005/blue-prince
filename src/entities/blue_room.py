# Blueprint
from src.entities.room import Room
from src.entities.door import Door
from abc import abstractmethod
from src.entities.player import Player
from src.utils.rarity import Rarity
from src.entities.other_item import OtherItem
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.entities.bunny_paw import BunnyPaw
from src.utils.lock_state import LockState
from src.utils.direction import Direction

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
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, possible_items = [], img_path: str = ''):
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path = img_path)
    @abstractmethod
    def on_enter(self, player):
        return super().on_enter(player)
    
    @abstractmethod
    def on_draft(self, player):
        return super().on_draft(player)

    def apply_effect(self, player: Player):
        if self.name == "Nook":
            player.add_keys(1)
        elif self.name == "Den":
            player.add_gems(1)
        elif self.name == "Pantry":
            player.add_money(4)
        elif self.name == "Antechamber":
            print("You Win") # Maybe we can add a fon win in game to restart the game or insert a funny photo 

class EntranceHall(BlueRoom):
    def __init__(self):
        name = "Entrance Hall"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.TOP),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
            Door(LockState.DOUBLE_LOCKED, Direction.RIGHT),
        ]
        rarity = Rarity.COMMON
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items)
    
    def on_enter(self, player: Player):
        # WIN
        pass
    
    def on_draft(self, player):
        pass

class Parlor(BlueRoom):
    def __init__(self):
        name = "Parlor"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
        ]
        rarity = Rarity.COMMON
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items)
    
    def on_enter(self, player: Player):
        # WIN
        pass
    
    def on_draft(self, player):
        pass

class Nook(BlueRoom):
    def __init__(self):
        name = "Nook"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
        ]
        rarity = Rarity.COMMON
        possible_items = [] # To define
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items)
    
    def on_enter(self, player: Player):
        if (self.visited): return
        player.add_keys(1)
        self.visited = True
    
    def on_draft(self, player):
        return super().on_draft(player)
    
class Den(BlueRoom):
    def __init__(self):
        name = "Den"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
            Door(LockState.DOUBLE_LOCKED, Direction.RIGHT)
        ]
        rarity = Rarity.COMMON
        possible_items = []
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items)
    
    def on_enter(self, player: Player):
        if (self.visited): return
        player.add_gems(1)
        self.visited = True
    
    def on_draft(self, player):
        return super().on_draft(player)

class Pantary(BlueRoom):
    def __init__(self):
        name = "Pantary"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
        ]
        rarity = Rarity.COMMON
        possible_items = []
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items)
    
    def on_enter(self, player: Player):
        if (self.visited): return
        player.add_money(4)
        self.visited = True
    
    def on_draft(self, player):
        return super().on_draft(player)

class Antechamber(BlueRoom):  
    def __init__(self):
        name = "Antechamber"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
            Door(LockState.DOUBLE_LOCKED, Direction.RIGHT),
        ]
        rarity = Rarity.COMMON
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items)
    
    def on_enter(self, player: Player):
        # WIN
        pass
    
    def on_draft(self, player):
        pass

class Closet(BlueRoom):  
    def __init__(self):
        name = "Closet"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
        ]
        rarity = Rarity.COMMON
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items)
    
    def on_enter(self, player: Player):
        pass
    
    def on_draft(self, player):
        pass