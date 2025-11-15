from src.entities.room import Room
from door import Door
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity
from src.entities.consumable_item import ConsumableItem

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
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, img_path: str):
        super().__init__(name, price, doors, rarity, img_path= spite, possible_items= possible_items)
        
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