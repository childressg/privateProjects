import pygame as pg
import random
import math

WIDTH = 1000
HEIGHT = 600
middle = pg.Vector2(WIDTH / 2, HEIGHT / 2)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

moveAccMag = 0.5
maxSpeed = 5
sprintMaxSpeed = 10
pos = pg.Vector2(WIDTH / 2, HEIGHT / 2)
vel = pg.Vector2(0, 0)

objectPositions = []
reach = 50

def start():
    for i in range(100):
        randX = random.randrange(-WIDTH, WIDTH * 2)
        randY = random.randrange(-HEIGHT, HEIGHT * 2)
        objectPositions.append(pg.Vector2(randX, randY))

def angleBetween(p1, p2):
    diff = p1 - p2
    angle = pg.Vector2(1, 0).angle_to(diff)
    return angle

def update(events):
    keys = pg.key.get_pressed()

    global vel
    global pos
    acc = pg.Vector2(0, 0)
    if keys[pg.K_w]:
        acc.y -= moveAccMag
    if keys[pg.K_s]:
        acc.y += moveAccMag
    if keys[pg.K_a]:
        acc.x -= moveAccMag
    if keys[pg.K_d]:
        acc.x += moveAccMag

    vel += acc
    if vel.magnitude() > 0:
        if keys[pg.K_LSHIFT]:
            vel = vel.clamp_magnitude(sprintMaxSpeed)
        else:
            vel = vel.clamp_magnitude(maxSpeed)
    pos += vel
    if acc.magnitude() == 0:
        vel *= 0.85
    if vel.magnitude() < 0.2:
        vel = pg.Vector2(0, 0)


    mousePos = pg.mouse.get_pos()

    angle = math.radians(180 - angleBetween(middle, pg.Vector2(mousePos[0], mousePos[1])))
    pg.draw.circle(screen, (0, 255, 0), mousePos, 2)
    # pg.draw.arc(screen, (255, 0, 0), (middle.x - 100, middle.y - 100, 200, 200), angle - math.radians(15), angle + math.radians(15), 45)

    mouseclicked = False
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                mouseclicked = True

    for i in range(len(objectPositions)):
        objectPosition = objectPositions[i]
        if isinstance(objectPosition, pg.Vector2):
            if mouseclicked and middle.distance_to(pg.Vector2(mousePos[0], mousePos[1])) < reach:
                if objectPosition.distance_to(mousePos + pos) <= 15:
                    randX = random.randrange(100, 200)
                    randY = random.randrange(100, 200)
                    objectPositions[i] = pg.Vector2(randX, randY)

        pg.draw.circle(screen, (0, 0, 255), objectPosition - pos, 15)

    pg.draw.circle(screen, 'white', middle, 10)

start()

while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    screen.fill((100, 200, 60))

    update(events)

    pg.display.flip()

    clock.tick(60)
