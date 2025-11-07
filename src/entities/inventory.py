# src/entities/inventory.py
from __future__ import annotations
from src.entities.object import Object
from src.entities.consumable_item import ConsumableItem
from src.entities.permanent_item import PermanentItem
from src.utils.consumable_type import ConsumableType


class Inventory:

    def __init__(self) -> None:
        # --- Core resources (fast access) ---
        # Movement points. Decrease by 1 on every valid move (Z/Q/S/D).

        
        self._steps: int = 70

        # Currencies & counters

        self._gold: int = 0
        self._gems: int = 2
        self._keys: int = 0
        self._dice: int = 0

        # --- Permanent abilities (flags toggled by permanent items) ---
        self._has_shovel: bool = False
        self._has_hammer: bool = False
        self._has_lock_pick: bool = False        # Open level-1 doors without spending a key
        self._has_metal_detector: bool = False   # Better loot odds (Mouhamed will hook into this)
        self._has_bunny_paw: bool = False        # Luck (more / better items; affects room/events)

        # --- Item collection aligned with Adam’s class tree ---
        self._objects: List[Object] = []

    
    # Read-only getters (keeps usage explicit and consistent)
    
    @property
    def steps(self) -> int:
        return self._steps

    @property
    def gold(self) -> int:
        return self._gold

    @property
    def gems(self) -> int:
        return self._gems

    @property
    def keys(self) -> int:
        return self._keys

    @property
    def dice(self) -> int:
        return self._dice

    @property
    def has_shovel(self) -> bool:
        return self._has_shovel

    @property
    def has_hammer(self) -> bool:
        return self._has_hammer

    @property
    def has_lock_pick(self) -> bool:
        return self._has_lock_pick

    @property
    def has_metal_detector(self) -> bool:
        return self._has_metal_detector

    @property
    def has_bunny_paw(self) -> bool:
        return self._has_bunny_paw

    @property
    def objects(self) -> List[Object]:
        # Return the list so UI can show it; gameplay should prefer the methods below.
        return self._objects

    
    # Mutators for movement points (used by Player/Level when moving or eating)
 
    def spend_steps(self, amount: int) -> None:
        """Lose movement points (cannot go below 0). Called after a successful move."""
        self._steps = max(0, self._steps - max(0, amount))

    def add_steps(self, amount: int) -> None:
        """Gain movement points (foods: +2, +3, +10, +15, +25)."""
        if amount > 0:
            self._steps += amount

    
    # Gem / Key / Dice / Gold helpers (used by Map, Events, and Items)
    

    def try_spend_gems(self, amount: int) -> bool:
        """Pay gem cost (e.g., choosing a room). Returns True on success."""
        if amount <= self._gems:
            self._gems -= amount
            return True
        return False

    def add_gems(self, amount: int) -> None:
        if amount > 0:
            self._gems += amount

    def try_spend_key(self) -> bool:
        """
        Spend a key if available. Map calls this when opening a locked door (level-2)
        or level-1 if we do not have a lock pick.
        """
        if self._keys > 0:
            self._keys -= 1
            return True
        return False

    def add_keys(self, amount: int) -> None:
        if amount > 0:
            self._keys += amount

    def try_spend_dice(self) -> bool:
        """Consume one dice to re-roll room choices."""
        if self._dice > 0:
            self._dice -= 1
            return True
        return False

    def add_dice(self, amount: int) -> None:
        if amount > 0:
            self._dice += amount

    def add_gold(self, amount: int) -> None:
        if amount > 0:
            self._gold += amount

    def try_spend_gold(self, amount: int) -> bool:
        if amount <= self._gold:
            self._gold -= amount
            return True
        return False

    
    # Permanent items (toggle abilities). 
    

    def grant_shovel(self) -> None:
        self._has_shovel = True

    def grant_hammer(self) -> None:
        self._has_hammer = True

    def grant_lock_pick(self) -> None:
        self._has_lock_pick = True

    def grant_metal_detector(self) -> None:
        self._has_metal_detector = True

    def grant_bunny_paw(self) -> None:
        self._has_bunny_paw = True

    
    # Item list management (keeps Adam’s tree happy + lets UI render an inventory)
    
    def _find_object_by_name(self, name: str) -> Optional[Object]:
        for obj in self._objects:
            # We assume Object exposes a public attribute or property 'name'.
            if getattr(obj, "name", None) == name:
                return obj
        return None

    def add_object(self, obj: Object) -> None:
        """
        Add an Object to the inventory. If a stack with the same name exists, merge quantities.
        Note: for permanent items we also toggle the corresponding ability flag.
        """
        # Merge stack if same name exists
        existing = self._find_object_by_name(getattr(obj, "name", ""))
        if existing is not None and hasattr(existing, "quantity") and hasattr(obj, "quantity"):
            existing.quantity += obj.quantity  # type: ignore[attr-defined]
        else:
            self._objects.append(obj)

        # If it’s a permanent item, toggle the right flag now
        if isinstance(obj, PermanentItem):
            self._apply_permanent_item_side_effect(obj)

        # If it’s a consumable with “automatic” effect (optional rule),
        # you could also apply side effects here. By default we don’t auto-consume.

    def remove_object(self, name: str, amount: int) -> bool:
        """Remove amount from an object stack; delete the stack if it reaches 0. Returns success."""
        target = self._find_object_by_name(name)
        if not target or not hasattr(target, "quantity"):
            return False

        if amount <= 0:
            return False

        if target.quantity < amount:  # type: ignore[attr-defined]
            return False

        target.quantity -= amount  # type: ignore[attr-defined]
        if target.quantity == 0:    # type: ignore[attr-defined]
            self._objects.remove(target)
        return True

   -
    # Applying item effects (called by Event/Room/Item logic)

    def apply_consumable(self, item: ConsumableItem) -> None:
        """
        Apply the effect of a consumable item once. Caller decides if the stack should be decremented.
        We rely on ConsumableType to route to the correct counter.
        """
        ctype = getattr(item, "_type", None)
        qty = getattr(item, "quantity", 1)

        
        if ctype == ConsumableType.step:
            self.add_steps(qty)
        elif ctype == ConsumableType.money:
            self.add_gold(qty)
        elif ctype == ConsumableType.gem:
            self.add_gems(qty)
        elif ctype == ConsumableType.key:
            self.add_keys(qty)
        elif ctype == ConsumableType.dice:
            self.add_dice(qty)
        else:
            # Unknown type → do nothing (or raise if you prefer strictness)
            pass

    def _apply_permanent_item_side_effect(self, item: PermanentItem) -> None:
        """
        Toggle flags for specific permanent items. We compare by class name so we can
        keep separate files (hammer.py, shovel.py, lock_pick.py, metal_detector.py, bunny_paw.py).
        """
        class_name = item.__class__.__name__.lower()
        if "shovel" in class_name:
            self.grant_shovel()
        elif "hammer" in class_name:
            self.grant_hammer()
        elif "lock" in class_name and "pick" in class_name:
            self.grant_lock_pick()
        elif "metal" in class_name and "detector" in class_name:
            self.grant_metal_detector()
        elif "bunny" in class_name or "paw" in class_name:
            self.grant_bunny_paw()
        # else: other permanent items could be added later

 # -------------------------------------------------------------------------
    # Convenience predicates used by Map/Rooms
 # -------------------------------------------------------------------------

    def can_open_level1_without_key(self) -> bool:
        """True if lock pick is owned (open level-1 doors for free)."""
        return self._has_lock_pick

    def has_any_permanent_tools(self) -> bool:
        return any([
            self._has_shovel, self._has_hammer, self._has_lock_pick,
            self._has_metal_detector, self._has_bunny_paw
        ])
