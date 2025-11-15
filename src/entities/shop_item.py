from src.entities.object import Object

class ShopItem:
    def __init__(self, object: Object, price):
        self.item = object
        self.price = price