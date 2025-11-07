from room import Room
class RoomPicker :
    def __init__(self, rooms: list[Room], refresh_price : int):
        self.__rooms = rooms
        self.__refresh_price = refresh_price

    @property
    def rooms(self):
        return self.__rooms
    @rooms.setter
    def rooms(self, rooms):
        self.__rooms = rooms

    @property
    def refresh_price(self):
        return self.__refresh_price
    @refresh_price.setter
    def refresh_price(self, refresh_price):
        self.__refresh_price = refresh_price
    
    