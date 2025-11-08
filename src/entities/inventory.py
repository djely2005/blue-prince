from dataclasses import dataclass

@dataclass
class Inventory:
    """Explicit names preferred. Counts start as per spec; adjust if design changes."""
    steps: int = 70
    gold: int = 0
    gems: int = 2
    keys: int = 0
    dice: int = 0

    # Permanent tools toggles:
    has_shovel: bool = False
    has_hammer: bool = False
    has_lock_pick: bool = False      # open level-1 doors for free
    has_metal_detector: bool = False # better loot chances
    has_bunny_paw: bool = False      # luck: more/better items

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

    def add_gold(self, n: int):
        self.gold += n

    def try_spend_gold(self, n: int) -> bool:
        """Return True if gold paid; else False (UI should block the choice)."""
        if self.gold > 0:
            self.gold -= n
            return True
        return False
    
    # I wanted to add a method that verify if the player had a permanent item
    # The purpose of LaundryRoom is trading gold, keys or gems
    def swap_gem_gold(self, choice: str):
        player_gold = self.gold
        player_gems = self.gems
        player_key = self.keys
        if choice == "SpinCycle":
            self.gold = player_gems
            self.gems = player_gold
        if choice == "washDry" :
            self.gems = player_key
            self.keys = player_gems
        if choice == "FliffFold":
            self.gold = player_key
            self.key = player_gold



