import pygame as pg

class Line:
    def __init__(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    @property
    def x1(self):
        return self._x1

    @property
    def y1(self):
        return self._y1

    @property
    def x2(self):
        return self._x2

    @property
    def y2(self):
        return self._y2

    def show(self, screen):
        pg.draw.line(screen, pg.Color('black'), (self.x1, self.y1), (self.x2, self.y2), 2)