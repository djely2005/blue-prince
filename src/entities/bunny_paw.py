from src.entities.permanent_item import PermanentItem
from src.utils.rarity import Rarity

class BunnyPaw(PermanentItem):
    def __init__(self):
        super().__init__('Bunny Paw', 1, rarity=Rarity.STANDARD)
        self.luck = 2.0
    def on_enter_inventory(self, player):
        player.luck += self.luck