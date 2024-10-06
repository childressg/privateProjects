from enum import Enum
from Item import item
from copy import copy

recipeList = []

def itemsFromNames(data):
    output = []
    for row in data:
        outRow = []
        for value in row:
            if value is None:
                outRow.append(None)
            else:
                outRow.append(item(value, None, None, None, None, None, None))
        output.append(outRow)
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
        for i in range(len(self._data)):
            for j in range(len(self._data[i])):
                if not testEntry(self._data[i][j], other._data[i][j]):
                    return False
        return True

    @property
    def outputItem(self):
        return self._outputItem

class recipeEnum(Enum):
    IRON_PICK = ([
        ["Iron", "Iron", "Iron"],
        [None, "Stone", None],
        [None, "Stone", None]
    ],
    item('Iron Pick', 1, "sprites/items/pickaxe.png", "pickaxe", "Isn't it Iron Pick?\nI'm gonna kill myself", 1, 10)
    )

    def __init__(self, data, outputItem):
        recipeList.append(Recipe(itemsFromNames(data), outputItem))

def checkRecipes(data):
    for recipe in recipeList:
        if recipe == Recipe(data, item(None, None, None, None, None, None, None)):
            return copy(recipe.outputItem)
    return None