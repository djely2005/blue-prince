from src.entities.object import Object

class ShopItem:
    def __init__(self, object: Object, price):
        self.item = object
        self.price = price
        # UI may mark an item as already owned by the player
        self.owned = False

    def mark_owned(self, value: bool = True):
        self.owned = value