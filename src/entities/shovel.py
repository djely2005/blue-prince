from src.entities.permanent_item import PermanentItem

class Shovel(PermanentItem):
    def __init__(self):
        super().__init__('Shovel', 1)