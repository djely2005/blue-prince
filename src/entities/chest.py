from src.entities.event import Event
from src.session import session
from src.entities.permanent_item import PermanentItem
from src.entities.lock_pick import LockPick
from src.entities.hammer import Hammer
from src.entities.consumable_item import ConsumableItem
from src.utils.consumable_type import ConsumableType
import random


class Chest(Event):
    """Chest event: can be opened with 1 key, a LockPick, or a Hammer. Gives
    better rewards than Locker. Single-use."""
    def __init__(self):
        super().__init__('Chest', 1, 'any')
        self.opened = False

    def _has_tool(self, player):
        has_lockpick = any((isinstance(p, LockPick) or getattr(p, 'name', '').lower() in ('lock pick','lockpick')) for p in player.inventory.permanentItems)
        has_hammer = any((isinstance(p, Hammer) or getattr(p, 'name', '').lower() == 'hammer') for p in player.inventory.permanentItems)
        return has_lockpick, has_hammer

    def open(self, player):
        if self.opened:
            return False, 'Already opened', {}

        inv = player.inventory
        has_lockpick, has_hammer = self._has_tool(player)
        # If hammer or lockpick present, they can open without spending a key
        if not has_lockpick and not has_hammer:
            if not inv.spend_keys(1):
                return False, 'Needs key, lock pick, or hammer to open', {}

        rnd = getattr(self, '_room_random', None) or session.random
        luck = max(1.0, getattr(player, 'luck', 1.0))

        # Better reward set
        money = rnd.randint(5, 15) * int(luck)
        gems = rnd.randint(1, 4) * int(luck)
        player.add_money(money)
        player.add_gems(gems)
        reward = {'money': money, 'gems': gems}

        # Higher chance for permanent
        if rnd.random() < min(0.6, 0.15 * luck):
            # give a Hammer or LockPick or MetalDetector
            choice = rnd.choice([Hammer, LockPick])
            item = choice(choice.__name__, 1)
            names = [getattr(p, 'name', '').lower() for p in player.inventory.permanentItems]
            if item.name.lower() not in names:
                player.inventory.add_permanent_item(item)
                reward['permanent'] = item

        self.opened = True
        return True, 'Chest opened', reward