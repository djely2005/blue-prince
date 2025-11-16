from src.entities.permanent_item import PermanentItem
from src.utils.rarity import Rarity
class Shovel(PermanentItem):
    def __init__(self):
        super().__init__('Shovel', 1, rarity=Rarity.STANDARD)