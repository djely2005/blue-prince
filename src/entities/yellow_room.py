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
import random
from src.entities.shovel import Shovel
from src.entities.metal_detector import MetalDetector
from src.entities.lock_pick import LockPick
from src.entities.hammer import Hammer
from src.entities.bunny_paw import BunnyPaw

from src.session import session


class YellowRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, possible_items = [], img_path: str = ''):
        # Possible Item to buy or exchange
        super().__init__(name, price, doors, rarity, session, possible_items= possible_items, img_path= img_path)

    # To open the shop I think we need to do it in main
    def on_enter(self, player):
        return super().on_enter(player)

    def on_draft(self, player):
        return super().on_draft(player)
# Find how to implement
class Commissary(YellowRoom):
    """A general shop where the player may buy items with money.

    Number of items and rarity depend on `player.luck`. Permanent items already
    owned by the player are marked via `ShopItem.owned = True` so the UI can label them.
    """
    def __init__(self, name: str = "Commissary", price: int = 0, doors: list[Door] = None, rarity: Rarity = Rarity.STANDARD, img_path: str = 'rooms/Commissary.webp'):
        doors = doors or [Door(LockState.LOCKED, Direction.BOTTOM), Door(LockState.LOCKED, Direction.LEFT)]
        super().__init__(name, price, doors, rarity, possible_items=[
            (Shovel, 'Shovel', 10),
            (MetalDetector, 'Metal Detector', 30),
            (LockPick, 'Lock Pick', 20),
            (Hammer, 'Hammer', 15),
            (BunnyPaw, 'Bunny Paw', 25),

        ], img_path=img_path)

    def on_draft(self, player: Player):
        # Build a deterministic dynamic shop inventory based on player.luck
        # Use the room-provided RNG set by Map (`_room_random`) if available, otherwise fall back to session RNG
        rnd = getattr(self, '_room_random', None) or getattr(self.session, 'random', None) or random.Random()

        luck = max(0.0, getattr(player, 'luck', 1.0))
        count = min(5, max(1, 1 + int(luck)))


        pool = list(self.possible_items)
        offers = []
        for _ in range(count):
            if not pool:
                break
            idx = rnd.randrange(len(pool))
            cls, label, base_price = pool.pop(idx)
            price = max(1, int(base_price * (1 + (0.2 * (luck - 1)))))
            item = cls()
            shop_item = ShopItem(item, price)
            # Mark as owned if player already has it
            for p in player.inventory.permanentItems:
                if getattr(p, 'name', None) == label:
                    shop_item.mark_owned(True)
                    break
            offers.append(shop_item)

        # Consumable offer (Gems) influenced by luck
        if rnd.random() < min(0.9, 0.25 + 0.15 * luck):
            offers.append(ShopItem(ConsumableItem('Gems', 1 + int(luck), ConsumableType.GEM), 5 * max(1, int(luck))))

        self.possible_items = offers[:5]
        return super().on_enter(player)


class LaundryRoom(YellowRoom):
    """Laundry Room: offers services (washing machines) that exchange resources.

    Services (each is a ShopItem with a price in money):
    - Service A: Exchange ALL Gems with ALL Money at 1:1 for cost 5 money
    - Service B: Exchange ALL Keys with ALL Gems at 1:1 for cost 5 money
    - Service C: Exchange ALL Keys with ALL Gold at 1:1 for cost 10 money
    """
    def __init__(self, name: str = 'Laundry Room', price: int = 0, doors: list[Door] = None, rarity: Rarity = Rarity.RARE, img_path: str = 'rooms/Laundry_Room.png'):
        doors = doors or [Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM), Door(LockState.DOUBLE_LOCKED, Direction.LEFT)]
        super().__init__(name, price, doors, rarity, possible_items=[], img_path=img_path)

    def on_draft(self, player: Player):
        # Build three service ShopItems. The ShopItem.item will be a simple dict describing the service
        services = []

        # Service A: Gems <-> Money exchange (pay 5 money to perform)
        services.append(ShopItem({'service': 'gems_to_money', 'desc': 'Exchange ALL Gems with ALL Money at 1:1'}, 5))

        # Service B: Keys -> Gems (swap all keys into gems 1:1) cost 5 money
        services.append(ShopItem({'service': 'keys_to_gems', 'desc': 'Exchange ALL Keys with ALL Gems at 1:1'}, 5))

        # Service C: Keys -> Gold (swap all keys into money at 1:1) cost 10 money
        services.append(ShopItem({'service': 'keys_to_money', 'desc': 'Exchange ALL Keys with ALL Gold at 1:1'}, 10))

        self.possible_item = services
        return super().on_enter(player)

    def perform_service(self, player: Player, service_key: str) -> bool:
        """Execute the specified service for the player.

        Returns True if performed, False if insufficient funds or invalid.
        """
        inv = player.inventory
        if service_key == 'gems_to_money':
            cost = 5
            if inv.money.quantity < cost:
                return False
            # pay cost
            inv.spend_money(cost)
            # Exchange all gems for money at 1:1 (add gems quantity to money and zero gems)
            amount = inv.gems.quantity
            inv.gems.quantity = 0
            inv.money.quantity += amount
            return True
        if service_key == 'keys_to_gems':
            cost = 5
            if inv.money.quantity < cost:
                return False
            inv.spend_money(cost)
            amount = inv.keys.quantity
            inv.keys.quantity = 0
            inv.gems.quantity += amount
            return True
        if service_key == 'keys_to_money':
            cost = 10
            if inv.money.quantity < cost:
                return False
            inv.spend_money(cost)
            amount = inv.keys.quantity
            inv.keys.quantity = 0
            inv.money.quantity += amount
            return True
        return False