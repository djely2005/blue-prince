from src.entities.event import Event

class Pit(Event):
    def __init__(self):
        super().__init__('Pit', 1)