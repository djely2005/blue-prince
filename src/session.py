import random
from src.entities.player import Player

class Session():
    def __init__(self, player:Player,seed: int):
        self.__seed = seed
        self.player = player
        self.random = random.Random(seed)

    @property
    def seed(self, seed):
        self.__seed = seed

    @seed.setter
    def seed(self):
        return self.__seed 
    
    def luck_radint(self, min_val, max_val):
        r = self.random.random()
        bias = 1 / (1 + self.player.luck)
        biased = r ** bias

        return int(min_val + biased * (max_val - min_val))