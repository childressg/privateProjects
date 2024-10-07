from Item import item
from enum import Enum
import pygame as pg

class objectEnum(Enum):
    STONE = (
        "Stone",
        5.0,
        "sprites/objects/stone.png",
        "sprites/objects/stone_outline.png",
        "sprites/objects/stone_flash.png",
        (50, 50),
        (25, 25),
        (0, 0),
        item("Stone", 1, "sprites/items/stone_item.png", "material", "Rock and Stone!")
    )
    IRON = (
        "Iron",
        10.0,
        "sprites/objects/iron.png",
        "sprites/objects/ore_outline.png",
        "sprites/objects/ore_flash.png",
        (50, 50),
        (25, 25),
        (0, 0),
        item("Iron", 1, "sprites/items/iron_item.png", "material", ":)")
    )
    GOLD = (
        "Gold",
        25.0,
        "sprites/objects/gold.png",
        "sprites/objects/ore_outline.png",
        "sprites/objects/ore_flash.png",
        (50, 50),
        (25, 25),
        (0, 0),
        item("Gold", 1, "sprites/items/gold_item.png", "material", "We're Rich!")
    )
    TREE = (
        "Tree",
        10.0,
        "sprites/objects/tree.png",
        "sprites/objects/tree_outline.png",
        "sprites/objects/tree_trunk_flash.png",
        (50 ,100),
        (25, 92),
        (0, 70),
        item("Wood", 1, "sprites/items/stone_item.png", "material", "splintery")
    )

    def __init__(self, name, max_health, main_path, outline_path, flash_path, image_size, image_offset, bar_offset, drop_item):
        self._name = name
        self._max_health = max_health
        self._main_path = main_path
        self._outline_path = outline_path
        self._flash_path = flash_path
        self._dropItem = drop_item
        self._image_size = image_size
        self._image_offset = image_offset
        self._bar_offset = bar_offset

    @property
    def name(self):
        return self._name

    @property
    def max_health(self):
        return self._max_health

    @property
    def main_path(self):
        return self._main_path

    @property
    def outline_path(self):
        return self._outline_path

    @property
    def flash_path(self):
        return self._flash_path

    @property
    def dropItem(self):
        return self._dropItem

    @property
    def image_size(self):
        return self._image_size

    @property
    def image_offset(self):
        return self._image_offset

    @property
    def bar_offset(self):
        return self._bar_offset

class Object:
    def __init__(self, objectInfo, position):
        if isinstance(objectInfo, objectEnum):
            self._health = objectInfo.max_health
            self._max_health = objectInfo.max_health
            self._images = (pg.transform.scale(pg.image.load(objectInfo.main_path).convert_alpha(), objectInfo.image_size),
                            pg.transform.scale(pg.image.load(objectInfo.outline_path).convert_alpha(), objectInfo.image_size),
                            pg.transform.scale(pg.image.load(objectInfo.flash_path).convert_alpha(), objectInfo.image_size))
            self._position = position
            self._flashTick = 0
            self._dropItem = objectInfo.dropItem
            self._offset = objectInfo.image_offset
            self._bar_offset = objectInfo.bar_offset
        else:
            print("Object object not created correctly!")

    @property
    def position(self):
        return self._position

    @property
    def images(self):
        return self._images

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
    def max_health(self):
        return self._max_health

    @property
    def flashTick(self):
        return self._flashTick

    @flashTick.setter
    def flashTick(self, flashTick):
        self._flashTick = flashTick

    @property
    def dropItem(self):
        return self._dropItem

    @property
    def offset(self):
        return self._offset

    @property
    def bar_offset(self):
        return self._bar_offset

    def display(self, imageNum, screen, loc):
        return screen.blit(self._images[imageNum], loc)