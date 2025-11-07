from abc import ABC


@ABC
class Object:
    def __init__(self, name: str, quantity: int):
        self._name = name
        self._quantity = quantity
    
    @property
    def name(self):
        return self._name
    @property.setter
    def name(self, name):
        self._name = name
    
    @property
    def quantity(self):
        return self._quantity
    @property.setter
    def quantity(self, quantity):
        self._quantity = quantity