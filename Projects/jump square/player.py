import pygame as pg


def line_line(x1, y1, x2, y2, x3, y3, x4, y4):
    denominator = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    if denominator == 0:
        return False, None, None
    uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
    uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

    if 0 <= uA <= 1 and 0 <= uB <= 1:
        intersectionX = x1 + (uA * (x2-x1))
        intersectionY = y1 + (uA * (y2-y1))
        return True, intersectionX, intersectionY

    return False, None, None


def line_rect(x1, y1, x2, y2, rx, ry, rw, rh):
    left = line_line(x1, y1, x2, y2, rx, ry, rx, ry + rh)
    right = line_line(x1, y1, x2, y2, rx + rw, ry, rx + rw, ry + rh)
    top = line_line(x1, y1, x2, y2, rx, ry, rx + rw, ry)
    bottom = line_line(x1, y1, x2, y2, rx, ry + rh, rx + rw, ry + rh)

    intersections = (None if not left[0] else pg.Vector2(left[1], left[2]),
                     None if not right[0] else pg.Vector2(right[1], right[2]),
                     None if not top[0] else pg.Vector2(top[1], top[2]),
                     None if not bottom[0] else pg.Vector2(bottom[1], bottom[2]))
    return left[0] or right[0] or top[0] or bottom[0], intersections


class Player:
    def __init__(self, x, y, w, h):
        self._pos  = pg.Vector2(x, y)
        self._size = pg.Vector2(w, h)
        self._vel = pg.Vector2(0, 0)
        self._looking = 1

        self._on_ground = False
        self._ground_collision = pg.Vector2(w, 2)

    @property
    def pos(self):
        return self._pos

    @property
    def size(self):
        return self._size

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, v):
        self._vel = v

    @property
    def looking(self):
        return self._looking

    @property
    def on_ground(self):
        return self._on_ground

    def update(self, lines):
        self._pos += self._vel
        if not self._on_ground:
            self._vel += pg.Vector2(0, .4)
        else:
            self._vel = pg.Vector2(0, 0)
        if self._vel.y > 10:
            self._vel.y = 10

        self.check_collision(lines)

    def show(self, screen):
        pg.draw.rect(screen, pg.Color('red'), (self.pos, self.size))
        pg.draw.rect(screen, pg.Color('black'), (self.pos, self.size), 2)

    def check_collision(self, lines):
        touching = False
        for line in lines:
            if not self._on_ground:
                line_collide = line_rect(line.x1, line.y1, line.x2, line.y2, self.pos.x, self.pos.y, self.size.x, self.size.y)
                if line_collide[0]:
                    self._vel = pg.Vector2(0, 0)
                    self.move(line, line_collide[1])
            if line_rect(line.x1, line.y1, line.x2, line.y2, self.pos.x, self.pos.y + self.size.y, self._ground_collision.x, self._ground_collision.y)[0]:
                touching = True
        self._on_ground = touching

    def move(self, line, intersections):
        slope = None if line.x1 == line.x2 else (line.y1 - line.y2) / (line.x2 - line.x1)
        if slope is None: # vetical line
            pass
        elif slope <= 0:
            left_most = None
            for intersection in intersections:
                if intersection is not None:
                    if left_most is None:
                        left_most = intersection
                    else:
                        if left_most.x > intersection.x:
                            left_most = intersection
            self._pos = left_most - pg.Vector2(0, self.size.x)
        else:
            right_most = None
            for intersection in intersections:
                if intersection is not None:
                    if right_most is None:
                        right_most = intersection
                    else:
                        if right_most.x > intersection.x:
                            right_most = intersection
            self._pos = right_most - self.size

    @property
    def on_ground(self):
        return self._on_ground

    def jump(self, left, power):
        max_power = -10
        direction = -1 if left else 1
        self._vel = pg.Vector2(5 * direction, max_power * power)
        self._on_ground = False
