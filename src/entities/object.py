from abc import ABC


@ABC
class Object:
    def __init__(self, name: str, quantity: int):
        self._name = name
        self._quantity = quantity