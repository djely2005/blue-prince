from dataclasses import dataclass
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.utils.consumable_type import ConsumableType
# Should we reconsider the implementation of inventory ?
# I think we need a better structure
class Inventory:
    def __init__(self):
        """Explicit names preferred. Counts start as per spec; adjust if design changes."""
        self.permanentItems: PermanentItem = []
        self.steps: ConsumableItem = ConsumableItem('Steps', 70, ConsumableType.STEP)
        self.money: ConsumableItem = ConsumableItem('Money', 0, ConsumableType.MONEY)
        self.gems: ConsumableItem = ConsumableItem('Gems', 0, ConsumableType.GEM)
        self.keys: ConsumableItem = ConsumableItem('keys', 0, ConsumableType.KEY)
        self.dice: ConsumableItem = ConsumableItem('Dice', 0, ConsumableType.DICE)
        pass
    # Needs to be private


    # Let's keep the method for later
    # We use clear verbs and explicit intent.
    def spend_steps(self, n: int) -> None:
        """Lose n steps. If steps reach 0, game over logic is handled by the scene/game loop."""
        self.steps.quantity = self.steps.quantity - n
        # Game should be over if negative

    def add_steps(self, n: int) -> None:
        """Foods add movement points (+2, +3, +10, +15, +25)."""
        self.steps.quantity += n

    def spend_gems(self, n: int) -> bool:
        """Return True if gems paid; else False (UI should block the choice)."""
        if self.gems.quantity >= n:
            self.gems.quantity -= n
            return True
        return False
    def add_gems(self, n: int) -> bool:
        self.gems.quantity += n

    def spend_keys(self) -> bool:
        """Consume a key if available."""
        if self.keys.quantity >= 0:
            self.keys.quantity -= 1
            return True
        return False

    def add_keys(self, n: int) -> bool:
        self.keys.quantity += n


    def spend_money(self, n: int) -> bool:
        """Return True if money paid; else False (UI should block the choice)."""
        if self.money.quantity >= n:
            self.money.quantity -= n
            return True
        return False
    
    def add_money(self, n: int):
        self.money.quantity += n
    # I wanted to add a method that verify if the player had a permanent item
    # The purpose of LaundryRoom is trading money, keys or gems
    # This method shouldn't be here
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



