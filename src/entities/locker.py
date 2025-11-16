from src.entities.event import Event
from src.session import session
from src.entities.permanent_item import PermanentItem
from src.entities.lock_pick import LockPick
from src.entities.hammer import Hammer
from src.entities.consumable_item import ConsumableItem
from src.utils.consumable_type import ConsumableType
import random


class Locker(Event):
    """Locker event: can be opened with 1 key or with a LockPick permanent item.
    Gives consumable and sometimes permanent rewards based on luck. Single-use.
    """
    def __init__(self):
        super().__init__('Locker', 1, 'blue')
        self.opened = False

    def _has_lockpick(self, player) -> bool:
        for p in player.inventory.permanentItems:
            if isinstance(p, LockPick) or getattr(p, 'name', '').lower() == 'lock pick' or getattr(p, 'name', '').lower() == 'lockpick':
                return True
        return False

    def open(self, player):
        if self.opened:
            return False, 'Already opened', {}

        inv = player.inventory
        used_key = False
        if self._has_lockpick(player):
            # use lockpick, doesn't consume it
            pass
        else:
            # try spending a key
            if not inv.spend_keys(1):
                return False, 'Needs a key or a Lock Pick to open', {}
            used_key = True

        rnd = getattr(self, '_room_random', None) or session.random
        luck = max(1.0, getattr(player, 'luck', 1.0))

        # Give moderate reward
        kind = rnd.choice(['GEM', 'MONEY'])
        if kind == 'GEM':
            amt = rnd.randint(1, 3) * int(luck)
            player.add_gems(amt)
            reward = {'gems': amt}
        else:
            amt = rnd.randint(2, 6) * int(luck)
            player.add_money(amt)
            reward = {'money': amt}

        # Small chance for a permanent (lower than chest)
        if rnd.random() < min(0.3, 0.05 * luck):
            # give a LockPick occasionally
            item = LockPick('Lock Pick', 1)
            names = [getattr(p, 'name', '').lower() for p in player.inventory.permanentItems]
            if 'lock pick' not in names and 'lockpick' not in names:
                player.inventory.add_permanent_item(item)
                reward['permanent'] = item

        self.opened = True
        return True, 'Locker opened', reward