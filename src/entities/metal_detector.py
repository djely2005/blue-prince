from src.entities.permanent_item import PermanentItem
from src.utils.rarity import Rarity

class MetalDetector(PermanentItem):
    def __init__(self):
        super().__init__('Metal detector', 1, rarity=Rarity.STANDARD)