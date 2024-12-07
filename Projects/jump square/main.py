import pygame as pg
from player import Player
from line import Line

WIDTH, HEIGHT = 600, 600
MIDDLE = pg.Vector2(WIDTH / 2, HEIGHT / 2)
FPS = 60
DEBUG = True

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.NOFRAME)
pg.display.set_caption('jump square')

clock = pg.time.Clock()
running = True

line_locs = [(0, HEIGHT * 0.75, WIDTH, HEIGHT * 0.8)]
lines = []
p = Player(MIDDLE.x, MIDDLE.y, 20, 20)

debug = pg.font.SysFont('Arial', 15)

def draw_text(screen_object, font, string, loc, color):
    text = font.render(string, True, color)
    text_rect = text.get_rect()
    text_rect.topleft = loc
    screen_object.blit(text, text_rect)
    return text_rect.height

def start():
    for line_loc in line_locs:
        lines.append(Line(line_loc[0], line_loc[1], line_loc[2], line_loc[3]))

def update(events):
    for line in lines:
        line.show(screen)
    p.show(screen)

    if DEBUG:
        fps = clock.get_fps()
        draw_text(screen, debug, f"Fps: {fps:.2f}", pg.Vector2(0, 0), pg.Color('black'))
        draw_text(screen, debug, f"Pos: {str(p.pos)}", pg.Vector2(0, 15), pg.Color('black'))
        draw_text(screen, debug, f"Vel: {str(p.vel)}", pg.Vector2(0, 30), pg.Color('black'))
        draw_text(screen, debug, f"OnGround: {str(p.on_ground)}", pg.Vector2(0, 45), pg.Color('black'))

    p.update(lines)

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
                if p.on_ground:
                    p.vel = pg.Vector2(0, -10)
    screen.fill(pg.Color('white'))

    update(events)

    pg.display.flip()

    clock.tick(FPS)