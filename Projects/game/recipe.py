from enum import Enum
from Item import item
from copy import copy

from Projects.game.Item import ItemType

recipeList = []

def itemsFromNames(data):
    output = []
    for dataset in data:
        outset = []
        for row in dataset:
            outRow = []
            for value in row:
                if value is None:
                    outRow.append(None)
                else:
                    outRow.append(item(value, None, None, None, None, None, None))
            outset.append(outRow)
        output.append(outset)
    return output

def testEntry(this, other):
    if this is None:
        return other is None
    elif other is None:
        return False
    return this.name == other.name

class Recipe:
    def __init__(self, data, outputItem):
        self._data = data
        self._outputItem = outputItem

    def __eq__(self, other):
        for dataset in self._data:
            match = True
            for i in range(len(dataset)):
                for j in range(len(dataset[i])):
                    if not testEntry(dataset[i][j], other._data[0][i][j]):
                        match = False
            if match:
                return True
        return False

    @property
    def outputItem(self):
        return self._outputItem

class recipeEnum(Enum):
    IRON_PICK = ([[
        ["Iron", "Iron", "Iron"],
        [None, "Wood", None],
        [None, "Wood", None]
    ]],
                item('Iron Pick', 1, "sprites/items/pickaxe.png", ItemType.Tool, "Isn't it Iron Pick?\nI'm gonna kill myself", 1, 10)
    )
    IRON_AXE = ([[
        [None, "Iron", "Iron"],
        [None, "Wood", "Iron"],
        [None, "Wood", None]
    ],[
        ["Iron", "Iron", None],
        ["Iron", "Wood", None],
        [None, "Wood", None]
    ]],
                 item('Iron Axe', 1, "sprites/items/axe.png", ItemType.Tool,"sharp", 1, 10)
    )

    def __init__(self, data, outputItem):
        recipeList.append(Recipe(itemsFromNames(data), outputItem))

def checkRecipes(data):
    for recipe in recipeList:
        if recipe == Recipe(data, item(None, None, None, None, None, None, None)):
            return copy(recipe.outputItem)
    return None