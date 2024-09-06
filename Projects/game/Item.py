from sympy import false


class item:
    nextid = 0
    def __init__(self, name, count, primaryColor, secondaryColor, type, description, damage=None, durability=None):
        global nextid
        try:
            nextid
        except NameError:
            nextid = 0

        self._name = name
        self._count = count
        self._primaryColor = primaryColor
        self._secondaryColor = secondaryColor
        self._type = type
        self._description = description
        self._itemid = nextid
        self._damage = damage
        self._durability = durability
        nextid += 1

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        self._count = count

    @property
    def primaryColor(self):
        return self._primaryColor

    @property
    def secondaryColor(self):
        return self._secondaryColor

    @property
    def type(self):
        return self._type

    @property
    def description(self):
        return self._description

    @property
    def itemid(self):
        return self._itemid

    @property
    def damage(self):
        return self._damage

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, durability):
        self._durability = durability

    def __str__(self):
        return f"{self._name} | {self.count} | {self.primaryColor} | {self.secondaryColor}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, item):
            return false
        if self.type == "pickaxe":
            return self._itemid == other._itemid
        return self._name == other._name

    def __copy__(self):
        return item(self._name, self._count, self._primaryColor, self._secondaryColor, self._type, self._description, self._damage, self._durability)