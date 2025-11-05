from src.entities.permanent_item import PermanentItem

class Shovel(PermanentItem):
    def __init__(self, name: str, quantity: int):
        super().__init__(name, quantity)