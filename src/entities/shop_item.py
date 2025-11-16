from src.entities.object import Object
from src.entities.player import Player

class ShopItem:

    def __init__(self, label, price, effect):
        self.__label = label
        self.__price = price
        self.__effect = effect

    @property
    def label(self):
        return self.__label
    
    @property
    def price(self):
        return self.__price
    
    @property
    def effect(self):
        return self.__effect

    def buy(self, player: Player) -> bool:
        """Try to buy an item with gold and applying the effect"""

        if not player.inventory.spend_money(self.__price):
            return False

        self.__effect(player)
        return True

    

