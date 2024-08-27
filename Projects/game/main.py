import pygame as pg
import random
import math

from attr.validators import instance_of

WIDTH = 1000
HEIGHT = 600
fps = 60
middle = pg.Vector2(WIDTH / 2, HEIGHT / 2)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Something')
inventorySurface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
nameFont = pg.font.SysFont('Arial', 15)
countFont = pg.font.SysFont('Arial', 10)
clock = pg.time.Clock()
running = True

moveAccMag = 0.5
maxSpeed = 5
sprintMaxSpeed = 10
pos = pg.Vector2(0, 0)
vel = pg.Vector2(0, 0)

objectPositions = []
objectHealths = []
objectFlashTicks = []
objectFlashLength = 5
reach = 100

inventoryActive = False
inventorySize = 36
inventoryNames = []
inventoryCounts = []
inventoryIemPrimaryColor = {"Blue Stuff" : (0, 0, 255)}
inventoryIemSecondaryColor = {"Blue Stuff" : (0, 0, 100)}
inventorySorting = 'Name'

#function for finding an unoccupied location for a target
def randomPos():
    limits = (-WIDTH, WIDTH * 2, -HEIGHT, HEIGHT * 2)
    found = False

    while not found:

        randX = math.floor(random.randrange(limits[0], limits[1]))
        randY = math.floor(random.randrange(limits[2], limits[3]))
        newPos = pg.Vector2(randX, randY)

        if len(objectPositions) > 0:
            tooClose = False
            for objectPos in objectPositions:
                if isinstance(objectPos, pg.Vector2):
                    if objectPos.distance_to(newPos) < 30:
                        tooClose = True

            if not tooClose:
                found = True
                return newPos
        else:
            found = True
            return newPos

#start function
def start():
    for i in range(200):
        newPos = randomPos()
        objectPositions.append(newPos)
        objectHealths.append(10)
        objectFlashTicks.append(0)

#function to calculate angle between two points
def angleBetween(p1, p2):
    diff = p1 - p2
    angle = pg.Vector2(1, 0).angle_to(diff)
    return angle

#game loop function
def update(events):
    global inventoryActive
    global vel
    global pos
    keys = pg.key.get_pressed()

    acc = pg.Vector2(0, 0)
    # movement
    if not inventoryActive:
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

    #collision
    collisionpasses = 2
    for i in range(collisionpasses):
        for objectPos in objectPositions:
            if isinstance(objectPos, pg.Vector2):
                distance = middle.distance_to(objectPos - pos)
                if middle.distance_to(objectPos - pos) < 29:
                    angle = angleBetween(pos, objectPos)
                    distanceDiff = 30 - distance
                    pos -= pg.Vector2(math.cos(angle), math.sin(angle)) * distanceDiff
                    vel = pg.Vector2(0, 0)

    mousePos = pg.mouse.get_pos()

    # debug
    # angle = math.radians(180 - angleBetween(middle, pg.Vector2(mousePos[0], mousePos[1])))
    # pg.draw.circle(screen, (0, 255, 0), mousePos, 2)
    # pg.draw.arc(screen, (255, 0, 0), (middle.x - 100, middle.y - 100, 200, 200), angle - math.radians(15), angle + math.radians(15), 45)

    pg.draw.circle(screen, 'white', middle, 10)

    #mouse click
    mouseclicked = False
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                mouseclicked = True

    for i in range(len(objectPositions)):
        objectPosition = objectPositions[i]
        color = (0, 0, 255)

        if isinstance(objectPosition, pg.Vector2):
            distance = middle.distance_to(objectPosition - pos)
            if distance <= reach:

                pg.draw.circle(screen, (255, 255, 255), objectPosition - pos, 17)
                pg.draw.rect(screen, (255, 0, 0), [objectPosition - pos - pg.Vector2(17, 20), pg.Vector2(34, 5)])
                pg.draw.rect(screen, (0, 255, 0), [objectPosition - pos - pg.Vector2(17, 20), pg.Vector2(34 * (objectHealths[i] / 10), 5)])
                if mouseclicked:
                    if objectPosition.distance_to(mousePos + pos) <= 15:
                        objectHealths[i] -= 1
                        objectFlashTicks[i] = objectFlashLength
                        if objectHealths[i] <= 0:
                            newPos = randomPos()
                            objectPositions[i] = newPos
                            objectHealths[i] = 10
                            objectFlashTicks[i] = 0
                            if "Blue Stuff" not in inventoryNames:
                                inventoryNames.append("Blue Stuff")
                                inventoryCounts.append(1)
                            else:
                                inventoryCounts[inventoryNames.index("Blue Stuff")] += 1

        if objectFlashTicks[i] > 0:
            color = (255, 255, 255)
            objectFlashTicks[i] -= 1

        pg.draw.circle(screen, color, objectPosition - pos, 15)


    #inventory
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                if inventoryActive:
                    inventoryActive = False
                else:
                    inventoryActive = True

    if inventoryActive:
        pg.draw.rect(inventorySurface, (200, 200, 200, 230), [WIDTH * 0.05, HEIGHT * 0.1, WIDTH * 0.9, HEIGHT * 0.72]) # inventory background
        for i in range(4):
            for j in range(9):
                pg.draw.rect(inventorySurface, (150, 150, 150, 230), [WIDTH * 0.075 + WIDTH * 0.095 * j, HEIGHT * 0.145 + HEIGHT * 0.16 * i, WIDTH * 0.09, HEIGHT * 0.15]) # inventory slots
        for i, item in enumerate(inventoryNames):
            x = i % 9
            y = i // 9
            pg.draw.rect(inventorySurface, (220, 220, 220, 230), [WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.265 + HEIGHT * 0.16 * y, WIDTH * 0.09, HEIGHT * 0.03]) # item name background
            pg.draw.rect(inventorySurface, (220, 220, 220, 230), [WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.145 + HEIGHT * 0.16 * y, WIDTH * 0.02, HEIGHT * 0.034]) # item count background
            name = nameFont.render(item, 1, (0, 0, 0)) # item name
            nameRect = name.get_rect()
            nameRect.center = (WIDTH * 0.12 + WIDTH * 0.095 * x, HEIGHT * 0.28 + HEIGHT * 0.16 * y)
            count = countFont.render(str(inventoryCounts[i]), 1, (0, 0, 0)) # item count
            countRect = count.get_rect()
            countRect.center = (WIDTH * 0.085 + WIDTH * 0.095 * x, HEIGHT * 0.162 + HEIGHT * 0.16 * y)
            inventorySurface.blit(name, nameRect)
            inventorySurface.blit(count, countRect)
            pg.draw.circle(inventorySurface, inventoryIemSecondaryColor[item],(WIDTH * 0.13 + WIDTH * 0.095 * x, HEIGHT * 0.208 + HEIGHT * 0.16 * y), WIDTH * 0.025) # secondary color circle
            pg.draw.circle(inventorySurface, inventoryIemPrimaryColor[item],(WIDTH * 0.13 + WIDTH * 0.095 * x, HEIGHT * 0.208 + HEIGHT * 0.16 * y), WIDTH * 0.02) # primary color circle


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

    screen.fill((100, 200, 60))
    inventorySurface.fill((255, 255, 255, 0))

    update(events)

    screen.blit(inventorySurface, (0, 0))


    pg.display.flip()

    clock.tick(fps)
