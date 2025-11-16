from src.entities.event import Event

class Locker(Event):
    def __init__(self):
        super().__init__('Locker', 1)