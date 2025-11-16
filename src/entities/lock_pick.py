from src.entities.permanent_item import PermanentItem
from src.utils.rarity import Rarity

class LockPick(PermanentItem):
    def __init__(self):
        super().__init__('Lock pick', 1, rarity=Rarity.STANDARD)