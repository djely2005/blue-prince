from dataclasses import dataclass
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.utils.consumable_type import ConsumableType
# Should we reconsider the implementation of inventory ?
# I think we need a better structure
@dataclass
class Inventory:
    """Explicit names preferred. Counts start as per spec; adjust if design changes."""
    permanentItems: PermanentItem = []
    steps: ConsumableItem = ConsumableItem('Steps', 70, ConsumableType.STEP)
    money: ConsumableItem = ConsumableItem('Money', 0, ConsumableType.MONEY)
    gems: ConsumableItem = ConsumableItem('Gems', 0, ConsumableType.GEM)
    keys: ConsumableItem = ConsumableItem('keys', 0, ConsumableType.KEY)
    dice: ConsumableItem = ConsumableItem('Dice', 0, ConsumableType.DICE)


    # Let's keep the method for later
    # We use clear verbs and explicit intent.
    def spend_steps(self, n: int) -> None:
        """Lose n steps. If steps reach 0, game over logic is handled by the scene/game loop."""
        self.steps = max(0, self.steps - n)

    def add_steps(self, n: int) -> None:
        """Foods add movement points (+2, +3, +10, +15, +25)."""
        self.steps += n

    def try_spend_gems(self, n: int) -> bool:
        """Return True if gems paid; else False (UI should block the choice)."""
        if self.gems >= n:
            self.gems -= n
            return True
        return False

    def try_spend_key(self) -> bool:
        """Consume a key if available."""
        if self.keys > 0:
            self.keys -= 1
            return True
        return False

    def can_open_level1_for_free(self) -> bool:
        """Lock pick allows level-1 doors without consuming a key."""
        return self.has_lock_pick
    # Maybe it's needed when we entry a room or a shop
    def lose_steps(self, n :int):
        self.steps -= n

    def add_keys(self, n: int):
        self.keys += n

    def add_gems(self, n: int):
        self.gems += n

    def add_money(self, n: int):
        self.money += n

    def try_spend_money(self, n: int) -> bool:
        """Return True if money paid; else False (UI should block the choice)."""
        if self.money > 0:
            self.money -= n
            return True
        return False
    
    # I wanted to add a method that verify if the player had a permanent item
    # The purpose of LaundryRoom is trading money, keys or gems
    def swap_gem_money(self, choice: str):
        player_money = self.money
        player_gems = self.gems
        player_key = self.keys
        if choice == "SpinCycle":
            self.money = player_gems
            self.gems = player_money
        if choice == "washDry" :
            self.gems = player_key
            self.keys = player_gems
        if choice == "FliffFold":
            self.money = player_key
            self.keys = player_money



