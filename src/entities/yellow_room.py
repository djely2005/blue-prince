from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.utils.rarity import Rarity
from src.entities.inventory import Inventory

class YellowRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, interactables: list[Object]=[]):
        super().__init__(name, price, doors, rarity, interactables)

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