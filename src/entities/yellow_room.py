from abc import ABC, abstractmethod
from src.entities.room import Room
from src.entities.door import Door
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.consumable_item import ConsumableItem
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.entities.shop_item import ShopItem
from src.entities.player import Player
from src.utils.consumable_type import ConsumableType
from src.entities.permanent_item import PermanentItem
from src.utils.permanent_type import PermanentType

class YellowRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, possible_items = [], img_path: str = ''):
        # Possible Item to buy or exchange
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= img_path)
        self.shop_items: list[ShopItem] = []

    @abstractmethod
    def on_enter(self, player):
        return super().on_enter(player)
    
    @abstractmethod
    def on_draft(self, player):
        return super().on_draft(player)
    
    def shop(self, player: Player, choice: str) -> bool:
        """Shop logic using shopitem"""
        for item in self.shop_items:
            if item.label == choice:
                return item.buy(player)
        return False
    
    def apply_effect(self, player):
        pass

class LaundryRoom(YellowRoom):
    def __init__(self, player):
        name = "Laundry Room"
        price = 1
        doors = [Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM)]
        rarity = Rarity.RARE
        sprite_path = "rooms/laundry_room.png"
        possible_items = [
                            (0.27, ConsumableItem, {'name': 'Gold', 'quantity': 1}),
                            (0.25, ConsumableItem, {'name': 'Gold', 'quantity': 2}),
                            (0.23, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
                            (0.20, ConsumableItem, {'name': 'Gold', 'quantity': 4}),
                            (0.17, ConsumableItem, {'name': 'Gold', 'quantity': 5}),
                            (0.15, ConsumableItem, {'name': 'Gold', 'quantity': 6}),
                            (0.15, ConsumableItem, {'name': 'Key', 'quantity': 1})
        ]   
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)
    
    def on_draft(self, player):
        pass
    
    def on_enter(self, player):
        self.shop_items = [
            ShopItem(
                label="Spin Cycle",
                price=5,
                effect=lambda p: p.inventory.swap_resources("Spin Cycle")
            ),
            ShopItem(
                label="Wash & Dry",
                price=5,
                effect=lambda p: p.inventory.swap_resources("Wash & Dry")
            ),
            ShopItem(
                label="Fluff & Fold",
                price=10,
                effect=lambda p: p.inventory.swap_resources("Fluff & Fold")
            ),
        ]
    
class Locksmith(YellowRoom):
    def __init__(self):
        name = "Locksmith"
        price = 1
        doors = [Door(LockState.UNLOCKED, Direction.BOTTOM)]
        rarity = Rarity.UNUSUAL
        sprite_path = "rooms/Locksmith.png"
        possible_items = [
                        (0.25, ConsumableItem, {'name': 'Gold', 'quantity': 2}),
                        (0.20, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
                        (0.15, ConsumableItem, {'name': 'Gold', 'quantity': 5}),
                        (0.2, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
                        (0.15, ConsumableItem, {'name': 'Key', 'quantity': 1})
    ]
        
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= sprite_path)

    def on_draft(self, player):
        pass
    
    def on_enter(self, player):
        self.shop_items = [
            ShopItem(
                label="Key",
                price=5,
                effect=lambda p: p.inventory.add_keys(1)
            ),
            ShopItem(
                label="Set of Keys",
                price=12,
                effect=lambda p: p.inventory.add_keys(3)
            ),
            ShopItem(
                label="Lockpick",
                price=10,
                effect=self._give_lockpick
            ),
        ]
    
    def _give_lockpick(self, player: Player):
        """Effect only possible if player buys lockpick """
        if not player.has_lock_pick: # Flase meaning he doesn't have one
            player.has_lock_pick = True
