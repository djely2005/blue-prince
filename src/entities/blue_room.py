# Blueprint
from src.entities.room import Room
from src.entities.door import Door
from abc import abstractmethod
from src.entities.player import Player
from src.utils.rarity import Rarity
from src.entities.consumable_item import ConsumableItem
from src.utils.consumable_type import ConsumableType
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.session import session

class BlueRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, possible_items = [], img_path: str = ''):
        # Keep session passed through to Room; BlueRoom adds no extra state currently
        super().__init__(name, price, doors, rarity, session, possible_items= possible_items, img_path = img_path)

    @abstractmethod
    def on_enter(self, player):
        return super().on_enter(player)
    
    @abstractmethod
    def on_draft(self, player):
        return super().on_draft(player)
    
    @abstractmethod
    def shop(self, player, choice: str):
        return super().shop(player)


class EntranceHall(BlueRoom):
    def __init__(self):
        name = "Entrance Hall"
        price = 0
        doors = [
            Door(LockState.UNLOCKED, Direction.TOP),
            Door(LockState.UNLOCKED, Direction.LEFT),
            Door(LockState.UNLOCKED, Direction.RIGHT),
        ]
        rarity = Rarity.COMMON
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path='rooms/Entrance_Hall.webp')
    
    def on_enter(self, player: Player):
        # Starting room: mark visited on entry
        self.visited = True
    
    def on_draft(self, player):
        pass
    
    def shop(self, player, choice: str):
        return super().shop(player, choice)


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
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path='rooms/Parlor.webp')
    
    def on_enter(self, player: Player):
        # Neutral room — mark visited on entry
        self.visited = True
    
    def on_draft(self, player):
        pass
    
    def shop(self, player, choice: str):
        return super().shop(player, choice)


class Nook(BlueRoom):
    def __init__(self):
        name = "Nook"
        price = 0
        # L-shaped: bottom + left (example)
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
        ]
        rarity = Rarity.COMMON
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path='rooms/Nook.png')
    
    def on_enter(self, player: Player):
        # Nook contains a single Key on first visit
        if self.visited:
            return
        player.add_keys(1)
        self.visited = True
    
    def on_draft(self, player):
        return super().on_draft(player)
    

class Den(BlueRoom):
    def __init__(self):
        name = "Den"
        price = 0
        # T-shaped: left, bottom, right (example)
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
            Door(LockState.DOUBLE_LOCKED, Direction.RIGHT)
        ]
        rarity = Rarity.COMMON
        possible_items = []
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path='rooms/Den.webp')
    
    def on_enter(self, player: Player):
        # Den contains a Gem on first visit
        if self.visited:
            return
        player.add_gems(1)
        self.visited = True
    
    def on_draft(self, player):
        return super().on_draft(player)
    
    def shop(self, player, choice: str):
        return super().shop(player, choice)


class Pantry(BlueRoom):
    def __init__(self):
        name = "Pantry"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
        ]
        rarity = Rarity.COMMON
        # possible_items tuples are (base_probability, item_class, init_kwargs)
        possible_items = [
            (1.0, ConsumableItem, { 'name': 'Gold', 'quantity': 4, 'type': ConsumableType.MONEY }),
            (0.8, ConsumableItem, { 'name': 'Apple', 'quantity': 2, 'type': ConsumableType.STEP }),
            (0.6, ConsumableItem, { 'name': 'Banana', 'quantity': 3, 'type': ConsumableType.STEP }),
            (0.4, ConsumableItem, { 'name': 'Orange', 'quantity': 5, 'type': ConsumableType.STEP }),
        ]
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path='rooms/Pantry.png')
    
    def on_enter(self, player: Player):
        # Pantry contains a note and guaranteed loot on first visit:
        # guaranteed 4 Gold and at least one fruit (Apple/Banana/Orange).
        if self.visited:
            return

        # Add guaranteed gold
        gold = ConsumableItem('Gold', 4, ConsumableType.MONEY)
        self.available_items.append(gold)

        # Add at least one fruit. Currently deterministic: Apple.
        # Replace with random.choice(...) if you want variability.
        fruit = ConsumableItem('Apple', 2, ConsumableType.STEP)
        self.available_items.append(fruit)

        # Add a pantry note (informational)
        note = ConsumableItem('Pantry Note', 1, ConsumableType.DICE)
        self.available_items.append(note)

        self.visited = True
    
    def on_draft(self, player):
        return super().on_draft(player)
    
    def shop(self, player, choice: str):
        return super().shop(player, choice)


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
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path='rooms/Antechamber.webp')
    
    def on_enter(self, player: Player):
        # WIN
        pass
    
    def on_draft(self, player):
        pass
    
    def shop(self, player, choice: str):
        return super().shop(player, choice)


class Closet(BlueRoom):  
    def __init__(self):
        name = "Closet"
        price = 0
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
        ]
        rarity = Rarity.COMMON
        possible_items = [] # To define
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path='rooms/Closet.webp')
    
    def on_enter(self, player: Player):
        # Closet gives access to two items. Fill available_items with two common items if not visited.
        if self.visited:
            return
        common_items = [
            ConsumableItem('Apple', 2, ConsumableType.STEP),
            ConsumableItem('Gold', 1, ConsumableType.MONEY),
            ConsumableItem('Key', 1, ConsumableType.KEY),
            ConsumableItem('Gem', 1, ConsumableType.GEM),
        ]
        # Pick first two to keep deterministic; can be randomized later
        self.available_items.append(common_items[0])
        self.available_items.append(common_items[1])
        self.visited = True
    
    def on_draft(self, player):
        pass
    
    def shop(self, player, choice: str):
        return super().shop(player, choice)