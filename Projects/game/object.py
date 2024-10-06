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
        50,
        50,
        1,
        "Rock and Stone!",
        "sprites/items/stone_item.png"
    )
    IRON = (
        "Iron",
        10.0,
        "sprites/objects/iron.png",
        "sprites/objects/ore_outline.png",
        "sprites/objects/ore_flash.png",
        50,
        50,
        1,
        "Rusty rock of potential.",
        "sprites/items/iron_item.png"
    )
    GOLD = (
        "Gold",
        25.0,
        "sprites/objects/gold.png",
        "sprites/objects/ore_outline.png",
        "sprites/objects/ore_flash.png",
        50,
        50,
        1,
        "We're Rich!",
        "sprites/items/gold_item.png"
    )

    def __init__(self, name, max_health, main_path, outline_path, flash_path, image_width, image_height, drop_count, description, item_path):
        self._name = name
        self._max_health = max_health
        self._main_path = main_path
        self._outline_path = outline_path
        self._flash_path = flash_path
        self._dropItem = item(name, drop_count, item_path, "material", description)
        self._image_width = image_width
        self._image_height = image_height

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
    def image_width(self):
        return self._image_width

    @property
    def image_height(self):
        return self._image_height

class Object:
    def __init__(self, objectInfo, position):
        if isinstance(objectInfo, objectEnum):
            self._health = objectInfo.max_health
            self._max_health = objectInfo.max_health
            self._images = (pg.transform.scale(pg.image.load(objectInfo.main_path).convert_alpha(), (objectInfo.image_width, objectInfo.image_height)),
                            pg.transform.scale(pg.image.load(objectInfo.outline_path).convert_alpha(), (objectInfo.image_width, objectInfo.image_height)),
                            pg.transform.scale(pg.image.load(objectInfo.flash_path).convert_alpha(), (objectInfo.image_width, objectInfo.image_height)))
            self._position = position
            self._flashTick = 0
            self._dropItem = objectInfo.dropItem
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

    def display(self, imageNum, screen, loc):
        screen.blit(self._images[imageNum], loc)