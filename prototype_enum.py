from enum import Enum


class Prototypes(Enum):
    WATER_MILL = 1
    TOWER = 2

    @classmethod
    def from_int(cls, value):
        for menu in cls:
            if menu.value == value:
                return menu
        raise ValueError("Invalid value",value)
