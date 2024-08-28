import pygame as pg
import random
import math

from patsy import origin
from scipy.special import euler

import Item
from inventory import inventory
from object import *

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
sortFont = pg.font.SysFont('Arial', 20)
clock = pg.time.Clock()
running = True

moveAccMag = 0.5
maxSpeed = 5
sprintMaxSpeed = 10
pos = pg.Vector2(0, 0)
vel = pg.Vector2(0, 0)

objectList = []
objectFlashLength = 5
reach = 100

pickaxeAngle = 90
swinging = False
swingingDown = True
swingSpeed = 5
upperAngle = 90
lowerAngle = 0

inventoryActive = False
inventory = inventory(36)

#function for finding an unoccupied location for a target
def randomPos():
    limits = (int(WIDTH * 0.6) + 15, int(WIDTH * 3.6) - 15, int(HEIGHT * -1) + 15, int(HEIGHT * 2) - 15)
    found = False

    while not found:

        randX = math.floor(random.randrange(limits[0], limits[1]))
        randY = math.floor(random.randrange(limits[2], limits[3]))
        newPos = pg.Vector2(randX, randY)

        if len(objectList) > 0:
            tooClose = False
            for object in objectList:
                objectPos = object.position
                if isinstance(objectPos, pg.Vector2):
                    if objectPos.distance_to(newPos) < 30:
                        tooClose = True

            if not tooClose:
                found = True
                return newPos
        else:
            found = True
            return newPos

def createObject(object):
    if isinstance(object, objectEnum):
        newPos = randomPos()
        objectList.append(Object(object, newPos))

#start function
def start():
    for i in range(500):
        if not random.randint(1, 4) == 4:
            createObject(objectEnum.STONE)
        else:
            createObject(objectEnum.IRON)

#function to calculate angle between two points
def angleBetween(p1, p2):
    diff = p1 - p2
    angle = pg.Vector2(1, 0).angle_to(diff)
    return angle

def rotate_on_pivot(image, angle, pivot, origin):
    surf = pg.transform.rotate(image, angle)

    offset = pivot + (origin - pivot).rotate(-angle)
    rect = surf.get_rect(center=offset)

    return surf, rect

#game loop function
def update(events):
    global inventoryActive
    global vel
    global pos
    global pickaxeAngle
    global swinging
    global swingingDown
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

    # #collision
    # collisionpasses = 2
    # for i in range(collisionpasses):
    #     for objectPos in objectPositions:
    #         if isinstance(objectPos, pg.Vector2):
    #             distance = middle.distance_to(objectPos - pos)
    #             if middle.distance_to(objectPos - pos) < 29:
    #                 angle = angleBetween(pos, objectPos)
    #                 distanceDiff = 30 - distance
    #                 pos -= pg.Vector2(math.cos(angle), math.sin(angle)) * distanceDiff
    #                 vel = pg.Vector2(0, 0)

    mousePos = pg.mouse.get_pos()
    mouseAngle = math.radians(180 - angleBetween(middle, pg.Vector2(mousePos[0], mousePos[1])))

    # debug

    # pg.draw.circle(screen, (0, 255, 0), mousePos, 2)
    # pg.draw.arc(screen, (255, 0, 0), (middle.x - 100, middle.y - 100, 200, 200), angle - math.radians(15), angle + math.radians(15), 45)

    pg.draw.rect(screen, (92, 70, 41), [WIDTH * 0.6 - pos.x, HEIGHT * -1 - pos.y, WIDTH * 3, HEIGHT * 3])
    armSurface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

    pg.draw.rect(armSurface, 'white', [middle.x, middle.y + 5, 20, 5])


    if swinging:
        if swingingDown:
            pickaxeAngle -= swingSpeed
            if pickaxeAngle <= lowerAngle:
                pickaxeAngle = lowerAngle
                swingingDown = False
        else:
            pickaxeAngle += swingSpeed
            if pickaxeAngle >= upperAngle:
                pickaxeAngle = upperAngle
                swingingDown = True
                swinging = False

    pickaxeRadius = 20
    startPos, endPos = pickaxeRadius * math.cos(math.radians(pickaxeAngle + 25)), pickaxeRadius * math.cos(math.radians(pickaxeAngle - 25))
    stickPos = pickaxeRadius * math.cos(math.radians(pickaxeAngle))
    pg.draw.line(armSurface, 'burlywood3', (middle.x + 20, middle.y + 7.5), (middle.x + 20 + stickPos, middle.y + 7.5), 2)
    pg.draw.line(armSurface, 'silver', (middle.x + 20 + startPos, middle.y + 7.5), (middle.x + 20 + endPos, middle.y + 7.5), 3)

    armRect = armSurface.get_rect()
    armSurface, rect = rotate_on_pivot(armSurface, math.degrees(mouseAngle), middle, middle)
    screen.blit(armSurface, rect)



    pg.draw.circle(screen, 'white', middle, 10)

    #mouse click
    mouseclicked = False
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                mouseclicked = True

    for object in objectList:
        objectPosition = object.position
        if isinstance(objectPosition, pg.Vector2):
            distance = middle.distance_to(objectPosition - pos)
            if distance <= reach:

                pg.draw.circle(screen, (255, 255, 255), objectPosition - pos, 17)
                pg.draw.rect(screen, (255, 0, 0), [objectPosition - pos - pg.Vector2(17, 25), pg.Vector2(34, 5)])
                pg.draw.rect(screen, (0, 255, 0), [objectPosition - pos - pg.Vector2(17, 25), pg.Vector2(34 * (object.health / object.maxHealth), 5)])
                if mouseclicked:
                    if objectPosition.distance_to(mousePos + pos) <= 15:
                        if not swinging:
                            swinging = True
                            object.health -= 1
                            object.flashTick = objectFlashLength
                            if object.health <= 0:
                                newPos = randomPos()
                                object.position = newPos
                                object.health = object.maxHealth
                                object.flashTick = 0
                                if isinstance(object.dropItem, Item.item):
                                    inventory.add(object.dropItem)
        if object.flashTick > 0:
            object.flashTick -= 1

        pg.draw.circle(screen, object.getColor()[1], object.position - pos, 15)
        pg.draw.circle(screen, object.getColor()[0], object.position - pos, 12)



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

        pg.draw.rect(inventorySurface, (85, 85, 85, 230), [WIDTH * 0.835, HEIGHT * 0.105, WIDTH * 0.06, HEIGHT * 0.035]) # sort method button
        sorting = sortFont.render(inventory.sortingType, 1, (255, 255, 255))
        sortRect = sorting.get_rect()
        sortRect.center = (WIDTH * 0.865, HEIGHT * 0.1220)
        if mouseclicked and sortRect.collidepoint(mousePos):
            if inventory.sortingType == "Name":
                inventory.sortingType = "Count"
            else:
                inventory.sortingType = "Name"

        inventorySurface.blit(sorting, sortRect)

        if mouseclicked and pg.Rect([WIDTH * 0.9, HEIGHT * 0.105, WIDTH * 0.021, HEIGHT * 0.035]).collidepoint(mousePos):
            if inventory.sortDown:
                inventory.sortDown = False
            else:
                inventory.sortDown = True

        pg.draw.rect(inventorySurface, (85, 85, 85, 230), [WIDTH * 0.9, HEIGHT * 0.105, WIDTH * 0.021, HEIGHT * 0.035]) # sort direction button
        if inventory.sortDown: # center = (WDITH * 0.9105, HEIGHT * 0.1225)
            pg.draw.polygon(inventorySurface, (255, 255, 255, 255), [(WIDTH * 0.92, HEIGHT *  0.114275), (WIDTH * 0.9105, HEIGHT *  0.130725), (WIDTH * 0.901, HEIGHT *  0.114275)], 1)
        else:
            pg.draw.polygon(inventorySurface, (255, 255, 255, 255),[(WIDTH * 0.92, HEIGHT * 0.130725), (WIDTH * 0.9105, HEIGHT * 0.114275), (WIDTH * 0.901, HEIGHT * 0.130725)], 1)


        for i in range(4):
            for j in range(9):
                pg.draw.rect(inventorySurface, (150, 150, 150, 230), [WIDTH * 0.075 + WIDTH * 0.095 * j, HEIGHT * 0.145 + HEIGHT * 0.16 * i, WIDTH * 0.09, HEIGHT * 0.15]) # inventory slots
        for i, item in enumerate(inventory.items):
            x = i % 9
            y = i // 9
            pg.draw.rect(inventorySurface, (220, 220, 220, 230), [WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.265 + HEIGHT * 0.16 * y, WIDTH * 0.09, HEIGHT * 0.03]) # item name background
            pg.draw.rect(inventorySurface, (220, 220, 220, 230), [WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.145 + HEIGHT * 0.16 * y, WIDTH * 0.02, HEIGHT * 0.034]) # item count background
            name = nameFont.render(item.name, 1, (0, 0, 0)) # item name
            nameRect = name.get_rect()
            nameRect.center = (WIDTH * 0.12 + WIDTH * 0.095 * x, HEIGHT * 0.28 + HEIGHT * 0.16 * y)
            count = countFont.render(str(item.count), 1, (0, 0, 0)) # item count
            countRect = count.get_rect()
            countRect.center = (WIDTH * 0.085 + WIDTH * 0.095 * x, HEIGHT * 0.162 + HEIGHT * 0.16 * y)
            inventorySurface.blit(name, nameRect)
            inventorySurface.blit(count, countRect)
            pg.draw.circle(inventorySurface, item.secondaryColor,(WIDTH * 0.13 + WIDTH * 0.095 * x, HEIGHT * 0.208 + HEIGHT * 0.16 * y), WIDTH * 0.025) # secondary color circle
            pg.draw.circle(inventorySurface, item.primaryColor,(WIDTH * 0.13 + WIDTH * 0.095 * x, HEIGHT * 0.208 + HEIGHT * 0.16 * y), WIDTH * 0.02) # primary color circle



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
