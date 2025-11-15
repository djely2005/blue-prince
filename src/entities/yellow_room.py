from src.entities.room import Room
from src.entities.door import Door
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.consumable_item import ConsumableItem
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.entities.shop_item import ShopItem
from src.entities.player import Player
from src.utils.consumable_type import ConsumableType
# !!!!!! THIS need to be verified because I did it before you defined the classes needed
# My structure : name_room: (probability, type, list[name, quantity])
possible_items = {
    "LaundryRoom": [
        (0.27, ConsumableItem, {'name': 'Gold', 'quantity': 1}),
        (0.25, ConsumableItem, {'name': 'Gold', 'quantity': 2}),
        (0.23, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
        (0.20, ConsumableItem, {'name': 'Gold', 'quantity': 4}),
        (0.17, ConsumableItem, {'name': 'Gold', 'quantity': 5}),
        (0.15, ConsumableItem, {'name': 'Gold', 'quantity': 6}),
        (0.15, ConsumableItem, {'name': 'Key', 'quantity': 1})
        # the first number is for probability I just did a random number we can change it later if needed
    ],
    "Kitchen": [
        (0.25, ConsumableItem, {'name': 'Gold', 'quantity': 2}),
        (0.20, ConsumableItem, {'name': 'Gold', 'quantity': 3}),
        (0.15, ConsumableItem, {'name': 'Gold', 'quantity': 5}),
        (0.2, ConsumableItem, {'name': 'Gem', 'quantity': 1}),
        (0.15, ConsumableItem, {'name': 'Key', 'quantity': 1})
    ]

}

class YellowRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, possible_items = [], img_path: str):
        # Possible Item to buy or exchange
        super().__init__(name, price, doors, rarity, possible_items= possible_items, img_path= spite)

    def apply_effect(self, player: Inventory, player_choice: str):
        if self.name == "Commissary" :
            pass

        elif self.name == "LaundryRoom":
            if player_choice:
                player.swap_gem_gold
        
        elif self.name == "Locksmith":
            if player_choice == "Key":
                if player.try_spend_gold(5):
                    player.add_keys(1)
            elif player_choice == "Set of Keys":
                if player.try_spend_gold(12):
                    player.add_keys(3)
            elif player_choice == "Special Key":
                if player.try_spend_gold(10) and player.has_lock_pick: # TRUE and FALSE
                    not player.has_lock_pick

    # To open the shop I think we need to do it in main


# Find how to implement
class LaundryRoom(YellowRoom):
    def __init__(self, player):
        name = "Laundry Room"
        price = 1
        doors = [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM)
        ]
        rarity = Rarity.RARE
        possible_items = [
            ShopItem(
                ConsumableItem("Gems", )
            )
        ]
        super().__init__(name, price, doors, rarity)
    def on_draft(self, player):
        return super().on_draft(player)
    def on_enter(self, player):
        self.possible_item = [
            ShopItem(
                ConsumableItem("Gems", self.__get_player_money() - 5, ConsumableType.GEM),
                self.__get_player_money()
            ),
            ShopItem(
                ConsumableItem("Keys", self.__get_player_money() - 5, ConsumableType.KEY),
                self.__get_player_money()
            ),
            ShopItem(
                ConsumableItem("Keys", self.__get_player_money() - 5, ConsumableType.KEY),
                self.__get_player_gems()
            ),

        ]
        return super().on_enter(player)
    def __get_player_gems(self, player: Player):
        return player.inventory.gems.quantity
    def __get_player_money(self, player: Player):
        return player.inventory.money.quantity