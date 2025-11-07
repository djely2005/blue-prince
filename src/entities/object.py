from abc import ABC


@ABC
class Object:
    def __init__(self, name: str, quantity: int):
        self.__name = name
        self.__quantity = quantity
    
    @property
    def name(self):
        return self.__name
    @property.setter
    def name(self, name):
        self.__name = name
    
    @property
    def quantity(self):
        return self.__quantity
    @property.setter
    def quantity(self, quantity):
        self.__quantity = quantity