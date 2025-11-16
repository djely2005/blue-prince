from src.entities.event import Event

class Chest(Event):
    def __init__(self):
        super().__init__('Chest', 1)