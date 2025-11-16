from src.entities.event import Event
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.entities.shovel import Shovel
from src.utils.consumable_type import ConsumableType
from src.session import session
import random


class Pit(Event):
    """Pit event: requires a Shovel permanent item to access. When opened
    it yields a small consumable reward and occasionally a permanent item
    depending on player.luck. Single-use (marks itself opened).
    """
    def __init__(self):
        super().__init__('Pit', 1, 'green')
        self.opened = False

    def can_access(self, player) -> bool:
        # Player needs a Shovel permanent item (by name)
        for p in player.inventory.permanentItems:
            if isinstance(p, Shovel) or getattr(p, 'name', '').lower() == 'shovel':
                return True
        return False

    def open(self, player):
        if self.opened:
            return False, 'Already opened', {}

        if not self.can_access(player):
            return False, 'Needs a Shovel to dig here', {}

        rnd = getattr(self, '_room_random', None) or session.random
        # Always give a small consumable reward influenced by luck
        luck = max(1.0, getattr(player, 'luck', 1.0))
        # Choose consumable type
        choices = ['MONEY', 'GEM', 'KEY', 'DICE']
        weights = [0.5, 0.2 * luck, 0.2 * luck, 0.1]
        kind = rnd.choices(choices, weights=weights, k=1)[0]
        if kind == 'MONEY':
            amount = rnd.randint(1, 5) * int(luck)
            player.add_money(amount)
            reward = {'money': amount}
        elif kind == 'GEM':
            amount = rnd.randint(1, 2) * int(luck)
            player.add_gems(amount)
            reward = {'gems': amount}
        elif kind == 'KEY':
            amount = rnd.randint(1, 1) * int(luck)
            player.add_keys(amount)
            reward = {'keys': amount}
        else:
            amount = 1
            player.add_dice(amount)
            reward = {'dice': amount}

        # Small chance to find a permanent item; luck increases chance
        perm_chance = min(0.5, 0.05 * luck)
        perm_found = None
        if rnd.random() < perm_chance:
            # choose a permanent item type to give
            perm_choices = [Shovel]
            cls = rnd.choice(perm_choices)
            item = cls('Shovel', 1)
            # If player already has similar permanent item, skip giving
            names = [getattr(p, 'name', '').lower() for p in player.inventory.permanentItems]
            if 'shovel' not in names:
                player.inventory.add_permanent_item(item)
                perm_found = item

        self.opened = True
        msg = 'You dig and find something.'
        if perm_found:
            msg += f' Also found permanent item: {perm_found.name}'
        return True, msg, reward