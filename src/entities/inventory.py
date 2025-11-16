from dataclasses import dataclass
from src.entities.permanent_item import PermanentItem
from src.entities.consumable_item import ConsumableItem
from src.utils.consumable_type import ConsumableType
from src.entities.lock_pick import LockPick
# Should we reconsider the implementation of inventory ?
# I think we need a better structure
class Inventory:
    def __init__(self):
        """Explicit names preferred. Counts start as per spec; adjust if design changes."""
        self.permanentItems: list[PermanentItem] = [
        ]
        self.otherItems: list = []  # Consumable items found in rooms
        self.steps: ConsumableItem = ConsumableItem('Steps', 70, ConsumableType.STEP)
        self.money: ConsumableItem = ConsumableItem('Money', 50, ConsumableType.MONEY)
        self.gems: ConsumableItem = ConsumableItem('Gems', 30, ConsumableType.GEM)
        self.keys: ConsumableItem = ConsumableItem('keys', 100, ConsumableType.KEY)
        self.dice: ConsumableItem = ConsumableItem('Dice', 20, ConsumableType.DICE)
        # Keep constructor minimal; avoid side-effects here.
    # Needs to be private

    def add_permanent_item(self, value: PermanentItem):
        self.permanentItems.append(value)
    # Let's keep the method for later
    # We use clear verbs and explicit intent.
    def spend_steps(self, n: int) -> None:
        """Lose n steps. If steps reach 0, game over logic is handled by the scene/game loop."""
        self.steps.quantity = max(0, self.steps.quantity - n)
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
    def add_gems(self, n: int) -> None:
        self.gems.quantity += n

    def spend_keys(self, n: int = 1) -> bool:
        """Consume `n` keys if available. Return True if spent, False otherwise."""
        if self.keys.quantity >= n:
            self.keys.quantity -= n
            return True
        return False

    def add_keys(self, n: int) -> None:
        self.keys.quantity += n


    def spend_money(self, n: int) -> bool:
        """Return True if money paid; else False (UI should block the choice)."""
        if self.money.quantity >= n:
            self.money.quantity -= n
            return True
        return False
    
    def add_money(self, n: int):
        self.money.quantity += n

    def spend_dice(self, n: int) -> bool:
        """Consume `n` dice if available. Return True if spent, False otherwise."""
        if self.dice.quantity >= n:
            self.dice.quantity -= n
            return True
        return False

    def add_dice(self, n: int) -> None:
        self.dice.quantity += n

    # I wanted to add a method that verify if the player had a permanent item
    # The purpose of LaundryRoom is trading money, keys or gems
    # This method shouldn't be here
    def swap_gem_money(self, choice: str):
        # Swap quantities in a controlled way rather than swapping objects.
        if choice == "SpinCycle":
            self.money.quantity, self.gems.quantity = self.gems.quantity, self.money.quantity
        elif choice == "washDry":
            # exchange gems for keys (example behaviour)
            self.gems.quantity, self.keys.quantity = self.keys.quantity, self.gems.quantity
        elif choice == "FliffFold":
            self.money.quantity, self.keys.quantity = self.keys.quantity, self.money.quantity

    def has_any_permanent_tools(self) -> bool:
        # Return True if any permanent items exist. Specific queries
        # (has_shovel, etc.) should be added if needed.
        return len(self.permanentItems) > 0

    def use_other_item(self, item) -> str:
        """Use/consume an OtherItem. Returns a message about the effect.
        Handles ConsumableItems and OtherItems based on their type.
        """
        
        # Get the item's type and quantity
        bonus = getattr(item, 'quantity', 5)
        item_type = getattr(item, 'type', None)
        
        # Apply the effect based on type
        if item_type and hasattr(item_type, 'name'):
            type_name = item_type.name
            if type_name == 'STEP':
                self.add_steps(bonus)
                msg = f"Used {item.name}! Gained {bonus} steps."
            elif type_name == 'MONEY':
                self.add_money(bonus)
                msg = f"Used {item.name}! Gained {bonus} money."
            elif type_name == 'GEM':
                self.add_gems(bonus)
                msg = f"Used {item.name}! Gained {bonus} gems."
            elif type_name == 'KEY':
                self.add_keys(bonus)
                msg = f"Used {item.name}! Gained {bonus} keys."
            else:
                msg = f"Used {item.name}!"
        else:
            # Default: assume steps
            self.add_steps(bonus)
            msg = f"Used {item.name}! Gained {bonus} steps."
        
        return msg