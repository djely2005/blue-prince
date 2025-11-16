from src.entities.permanent_item import PermanentItem
from src.utils.rarity import Rarity

class MetalDetector(PermanentItem):
    def __init__(self, name: str, quantity: int):
        super().__init__(name, quantity, rarity=Rarity.STANDARD)