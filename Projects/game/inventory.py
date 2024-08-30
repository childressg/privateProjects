from copy import copy
import Item

class inventory:
    def __init__(self, slots):
        self.slots = slots
        self._items = []
        self._sortingType = "Name"
        self._sortDown = False

    def sort(self):
        if self._sortingType == "Name":
            self._items.sort(key=lambda item: item.name, reverse=self._sortDown)
        elif self._sortingType == "Count":
            self._items.sort(key=lambda item: item.count, reverse=self._sortDown)

    def add(self, item):
        if item not in self._items:
            if not len(self._items) == self.slots:
                newItem = copy(item)
                self._items.append(newItem)
        else:
            existingItem = self._items[self._items.index(item)]
            if isinstance(existingItem, Item.item):
                existingItem.count += item.count
        self.sort()
    
    def remove(self, item):
        if item in self._items:
            if self._items[self._items.index(item)].count > item.count:
                existingItem = self._items[self._items.index(item)]
                if isinstance(existingItem, Item.item):
                    existingItem.count -= item.count
                self.sort()
                return True
            else:
                self._items.pop(self._items.index(item))
                self.sort()
        return False

    def find(self, itemId):
        for item in self._items:
            if item.itemid == itemId:
                return item
        return False
    @property
    def items(self):
        return self._items

    @property
    def sortingType(self):
        return self._sortingType

    @sortingType.setter
    def sortingType(self, value):
        self._sortingType = value
        self.sort()

    @property
    def sortDown(self):
        return self._sortDown

    @sortDown.setter
    def sortDown(self, value):
        self._sortDown = value
        self.sort()