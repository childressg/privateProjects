import math

import pygame as pg
from player import Player
from line import Line

WIDTH, HEIGHT = 600, 600
MIDDLE = pg.Vector2(WIDTH / 2, HEIGHT / 2)
FPS = 60
DEBUG = True

last_held = False
holding_space = False
facing_left = True
power = 0

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.NOFRAME)
pg.display.set_caption('jump square')

clock = pg.time.Clock()
running = True

line_locs = [(-WIDTH, HEIGHT * 0.8, 2 * WIDTH, HEIGHT * 0.8), (WIDTH / 2, HEIGHT * 0.2, WIDTH / 2, HEIGHT * 0.8)]
lines = []
p = Player(MIDDLE.x, MIDDLE.y, 20, 20)

debug = pg.font.SysFont('Arial', 15)

def draw_text(screen_object, font, string, loc, color):
    text = font.render(string, True, color)
    text_rect = text.get_rect()
    text_rect.topleft = loc
    screen_object.blit(text, text_rect)
    return text_rect.height

def draw_arrow(screen_object, start, end, d, l):
    theta = math.asin(d/l)
    lam = math.atan2(end[1] - start[1], end[0] - start[0])
    mu = -(lam + (math.pi - theta))
    mu2 = -mu + 2 * theta

    change = (l * math.cos(mu), l * math.sin(mu))
    change2 = (l * math.cos(mu2), -l * math.sin(mu2))

    pg.draw.line(screen_object, (0, 0, 0), start, end)
    pg.draw.line(screen_object, (0, 0, 0), end, (end[0] + change[0], end[1] - change[1]))
    pg.draw.line(screen_object, (0, 0, 0), end, (end[0] + change2[0], end[1] - change2[1]))

def start():
    for line_loc in line_locs:
        lines.append(Line(line_loc[0], line_loc[1], line_loc[2], line_loc[3]))

def update(events):
    global power
    global last_held
    for line in lines:
        line.show(screen)

    if DEBUG:
        fps = clock.get_fps()
        draw_text(screen, debug, f"Fps: {fps:.2f}", pg.Vector2(0, 0), pg.Color('black'))
        draw_text(screen, debug, f"Pos: {str(p.pos)}", pg.Vector2(0, 15), pg.Color('black'))
        draw_text(screen, debug, f"Vel: {str(p.vel)}", pg.Vector2(0, 30), pg.Color('black'))
        draw_text(screen, debug, f"OnGround: {str(p.on_ground)}", pg.Vector2(0, 45), pg.Color('black'))

    p.update(lines)

    if facing_left:
        draw_arrow(screen, p.pos + pg.Vector2(20, -10), p.pos + pg.Vector2(0, -10), 4, 5)
    else:
        draw_arrow(screen, p.pos + pg.Vector2(0, -10), p.pos + pg.Vector2(20, -10), 4, 5)

    if p.on_ground and holding_space and power < 100:
        power += 1

    p.show(screen)

    pg.draw.rect(screen, (0, 0, 0), pg.Rect(p.pos.x + 30, p.pos.y - 10, 5, 20))
    bar_height = 20 * (power / 100)
    pg.draw.rect(screen, (0, 255, 0), pg.Rect(p.pos.x + 30, p.pos.y - 10 + (20 - bar_height), 5, bar_height))

    if last_held and not holding_space and p.on_ground:
        p.jump(facing_left, power / 100)
        power = 0

    last_held = holding_space

start()

#game loop
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                holding_space = True
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                facing_left = True
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                facing_left = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                holding_space = False
    screen.fill(pg.Color('white'))

    update(events)

    pg.display.flip()

    clock.tick(FPS)