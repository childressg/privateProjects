from Item import item
from enum import Enum

class objectEnum(Enum):
    STONE = (
        "Stone",
        5.0,
        (173, 173, 173),
        (95, 95, 95),
        1,
        "Rock and Stone!"
    )
    IRON = (
        "Iron",
        10.0,
        (173, 173, 173),
        (205, 172, 151),
        1,
        "Rusty rock of potential."
    )
    GOLD = (
        "Gold",
        25.0,
        (173, 173, 173),
        (223, 197, 123),
        1,
        "We're Rich!"
    )

    def __init__(self, name, maxHealth, primaryColor, secondaryColor, dropCount, description):
        self._name = name
        self._maxHealth = maxHealth
        self._primaryColor = primaryColor
        self._secondaryColor = secondaryColor
        self._dropItem = item(name, dropCount, primaryColor, secondaryColor, "material", description)

    @property
    def name(self):
        return self._name

    @property
    def maxHealth(self):
        return self._maxHealth

    @property
    def primaryColor(self):
        return self._primaryColor

    @property
    def secondaryColor(self):
        return self._secondaryColor

    @property
    def dropItem(self):
        return self._dropItem

class Object:
    def __init__(self, objectInfo, position):
        if isinstance(objectInfo, objectEnum):
            self._health = objectInfo.maxHealth
            self._maxHealth = objectInfo.maxHealth
            self._colors = (objectInfo.primaryColor, objectInfo.secondaryColor)
            self._position = position
            self._flashTick = 0
            self._dropItem = objectInfo.dropItem
        else:
            print("Object object not created correctly!")


    def getColor(self):
        if self._flashTick > 0:
            return ((255, 255, 255), (255, 255, 255))
        else:
            return self._colors

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health

    @property
    def maxHealth(self):
        return self._maxHealth

    @property
    def flashTick(self):
        return self._flashTick

    @flashTick.setter
    def flashTick(self, flashTick):
        self._flashTick = flashTick

    @property
    def dropItem(self):
        return self._dropItem