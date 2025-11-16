from src.utils.consumable_type import ConsumableType
from src.entities.object import Object
from src.utils.rarity import Rarity

class PermanentItem(Object):
    def __init__(self, name: str, quantity: int, rarity: Rarity.COMMON):
        super().__init__(name, quantity, rarity=rarity)