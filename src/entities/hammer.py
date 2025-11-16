from src.entities.permanent_item import PermanentItem
from src.utils.rarity import Rarity

class Hammer(PermanentItem):
    def __init__(self):
        super().__init__('Hammer', 1, rarity=Rarity.STANDARD)