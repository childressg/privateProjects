import pygame as pg
import random
import math

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
infoNameFont = pg.font.SysFont('Arial', 20)
infoDescriptionFont = pg.font.SysFont('Arial', 17)
infoButtonsFont = pg.font.SysFont('Arial', 25)

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

#pickaxe variables
pickaxeAngle = 90
swinging = False
swingingDown = True
swingSpeed = 5
upperAngle = 90
lowerAngle = 0
mouseAngle = 0

inventoryActive = False
inventory = inventory(28)
selected = -1
equipped = -1
descriptionHeight = 0

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
        choice = random.choices([objectEnum.STONE, objectEnum.IRON, objectEnum.GOLD], [10, 4, 1])
        createObject(choice[0])
    inventory.add(Item.item('Iron Pick', 1, 'silver', 'burlywood3', "pickaxe", "Isn't it Iron Pick?\nI'm gonna kill myself"))

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
    global mouseAngle
    global selected
    global descriptionHeight
    global equipped

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

    if not inventoryActive:
        if vel.magnitude() > 0:
            if keys[pg.K_LSHIFT]:
                vel = vel.clamp_magnitude(sprintMaxSpeed)
            else:
                vel = vel.clamp_magnitude(maxSpeed)
        pos += vel
        if acc.magnitude() == 0:
            vel *= 0.85
        if vel.magnitude() < 0.1:
            vel = pg.Vector2(0, 0)


    mousePos = pg.mouse.get_pos()

    if not inventoryActive:
        mouseAngle = math.radians(180 - angleBetween(middle, pg.Vector2(mousePos[0], mousePos[1])))

    pg.draw.rect(screen, (50, 50, 50), [WIDTH * 0.58 - pos.x, HEIGHT * -1.035 - pos.y, WIDTH * 3.04, HEIGHT * 3.07])
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

    if equipped != -1:
        equippedItem = inventory.find(equipped)
        if isinstance(equippedItem, Item.item):
            pg.draw.line(armSurface, equippedItem.secondaryColor, (middle.x + 20, middle.y + 7.5),(middle.x + 20 + stickPos, middle.y + 7.5), 2)
            pg.draw.line(armSurface, equippedItem.primaryColor, (middle.x + 20 + startPos, middle.y + 7.5),(middle.x + 20 + endPos, middle.y + 7.5), 3)
    else:
        pg.draw.rect(armSurface, 'white', [middle.x + 15, middle.y + 5, stickPos, 5])

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
                if pg.mouse.get_pressed(3)[0] and not inventoryActive:
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
                    selected = -1
                else:
                    inventoryActive = True

    if inventoryActive:
        pg.draw.rect(inventorySurface, (200, 200, 200, 230), [WIDTH * 0.05, HEIGHT * 0.1, WIDTH * 0.9, HEIGHT * 0.72]) # inventory background

        pg.draw.rect(inventorySurface, (85, 85, 85, 230), [WIDTH * 0.645, HEIGHT * 0.105, WIDTH * 0.06, HEIGHT * 0.035]) # sort method button
        sorting = sortFont.render(inventory.sortingType, 1, (255, 255, 255))
        sortRect = sorting.get_rect()
        sortRect.center = (WIDTH * 0.675, HEIGHT * 0.1220)
        if mouseclicked and sortRect.collidepoint(mousePos):
            if inventory.sortingType == "Name":
                inventory.sortingType = "Count"
            else:
                inventory.sortingType = "Name"
            selected = -1

        inventorySurface.blit(sorting, sortRect)

        if mouseclicked and pg.Rect([WIDTH * 0.714, HEIGHT * 0.105, WIDTH * 0.021, HEIGHT * 0.035]).collidepoint(mousePos):
            if inventory.sortDown:
                inventory.sortDown = False
            else:
                inventory.sortDown = True
            selected = -1

        pg.draw.rect(inventorySurface, (85, 85, 85, 230), [WIDTH * 0.714, HEIGHT * 0.105, WIDTH * 0.021, HEIGHT * 0.035]) # sort direction button
        if inventory.sortDown:
            pg.draw.polygon(inventorySurface, (255, 255, 255, 255), [(WIDTH * 0.734, HEIGHT *  0.114275), (WIDTH * 0.7245, HEIGHT *  0.130725), (WIDTH * 0.715, HEIGHT *  0.114275)], 1)
        else:
            pg.draw.polygon(inventorySurface, (255, 255, 255, 255),[(WIDTH * 0.734, HEIGHT * 0.130725), (WIDTH * 0.7245, HEIGHT * 0.114275), (WIDTH * 0.715, HEIGHT * 0.130725)], 1)


        for i in range(4):
            for j in range(7):
                index = 7 * i + j
                if index == selected:
                    pg.draw.rect(inventorySurface, (100, 100, 100, 230), [WIDTH * 0.07 + WIDTH * 0.095 * j, HEIGHT * 0.135 + HEIGHT * 0.16 * i, WIDTH * 0.1, HEIGHT * 0.17])
                slot = pg.draw.rect(inventorySurface, (150, 150, 150, 230), [WIDTH * 0.075 + WIDTH * 0.095 * j, HEIGHT * 0.145 + HEIGHT * 0.16 * i, WIDTH * 0.09, HEIGHT * 0.15]) # inventory slots
                if mouseclicked and slot.collidepoint(mousePos):
                    if index < len(inventory.items):
                        selected = index

        for i, item in enumerate(inventory.items):
            x = i % 9
            y = i // 9
            pg.draw.rect(inventorySurface, (220, 220, 220, 230), [WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.265 + HEIGHT * 0.16 * y, WIDTH * 0.09, HEIGHT * 0.03]) # item name background
            name = nameFont.render(item.name, 1, (0, 0, 0)) # item name
            nameRect = name.get_rect()
            nameRect.center = (WIDTH * 0.12 + WIDTH * 0.095 * x, HEIGHT * 0.28 + HEIGHT * 0.16 * y)
            inventorySurface.blit(name, nameRect)

            if item.type == "material":
                pg.draw.rect(inventorySurface, (220, 220, 220, 230),[WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.145 + HEIGHT * 0.16 * y, WIDTH * 0.02,HEIGHT * 0.034])  # item count background
                count = countFont.render(str(item.count), 1, (0, 0, 0))  # item count
                countRect = count.get_rect()
                countRect.center = (WIDTH * 0.085 + WIDTH * 0.095 * x, HEIGHT * 0.162 + HEIGHT * 0.16 * y)
                inventorySurface.blit(count, countRect)
                pg.draw.circle(inventorySurface, item.secondaryColor,(WIDTH * 0.13 + WIDTH * 0.095 * x, HEIGHT * 0.208 + HEIGHT * 0.16 * y), WIDTH * 0.025) # secondary color circle
                pg.draw.circle(inventorySurface, item.primaryColor,(WIDTH * 0.13 + WIDTH * 0.095 * x, HEIGHT * 0.208 + HEIGHT * 0.16 * y), WIDTH * 0.02) # primary color circle
            if item.type == "pickaxe":
                pg.draw.rect(inventorySurface, item.primaryColor, [WIDTH * 0.09 + WIDTH * 0.095 * x, HEIGHT * 0.17 + HEIGHT * 0.16 * y, WIDTH * 0.06, HEIGHT * 0.025])
                pg.draw.rect(inventorySurface, item.secondaryColor, [WIDTH * 0.115 + WIDTH * 0.095 * x, HEIGHT * 0.195 + HEIGHT * 0.16 * y, WIDTH * 0.01, HEIGHT * 0.065])

        pg.draw.rect(inventorySurface, (180, 180, 180, 230), [WIDTH * 0.75, HEIGHT * 0.145, WIDTH * 0.185, HEIGHT * 0.63])

        pg.draw.rect(inventorySurface, (160, 160, 160, 230),[WIDTH * 0.76, HEIGHT * 0.16, WIDTH * 0.165, HEIGHT * 0.04]) # item name
        pg.draw.rect(inventorySurface, (160, 160, 160, 230),[WIDTH * 0.76, HEIGHT * 0.21, WIDTH * 0.165, HEIGHT * 0.27]) # item visual
        pg.draw.rect(inventorySurface, (160, 160, 160, 230),[WIDTH * 0.76, HEIGHT * 0.49, WIDTH * 0.165, descriptionHeight + HEIGHT * .02]) # item description

        if selected != -1:
            selectedItem = inventory.items[selected]
            if isinstance(selectedItem, Item.item):
                itemName = infoNameFont.render(selectedItem.name, 1, (0, 0, 0))  # item name
                itemNameRect = itemName.get_rect()
                itemNameRect.center = (WIDTH * 0.8425, HEIGHT * 0.18)
                inventorySurface.blit(itemName, itemNameRect)

                if selectedItem.type == "material":
                    center = (WIDTH * 0.8425, HEIGHT * 0.345)
                    pg.draw.circle(inventorySurface, selectedItem.secondaryColor, center, 50)
                    pg.draw.circle(inventorySurface, selectedItem.primaryColor, center, 40)
                if selectedItem.type == "pickaxe":
                    pg.draw.rect(inventorySurface, selectedItem.primaryColor,[WIDTH * 0.77, HEIGHT * 0.25, WIDTH * 0.145, HEIGHT * 0.05])
                    pg.draw.rect(inventorySurface, selectedItem.secondaryColor,[WIDTH * 0.8305, HEIGHT * 0.3, WIDTH * 0.024, HEIGHT * 0.17])

                lineList = selectedItem.description.split('\n')
                totalHeight = 0
                for line in lineList:
                    itemDescription = infoDescriptionFont.render(line, 1, (0, 0, 0)) # item description
                    itemDescriptionRect = itemDescription.get_rect()
                    itemDescriptionRect.midtop = (WIDTH * 0.8425, HEIGHT * 0.50 + totalHeight)
                    inventorySurface.blit(itemDescription, itemDescriptionRect)
                    totalHeight += itemDescriptionRect.height
                descriptionHeight = totalHeight

                if selectedItem.type == "pickaxe":
                    if equipped == selectedItem.itemid:
                        equipText = infoButtonsFont.render("Unequip", 1, (255, 255, 255))
                        equipButton = pg.draw.rect(inventorySurface, (85, 85, 85, 230),[WIDTH * 0.7925, HEIGHT * 0.71, WIDTH * 0.1, HEIGHT * 0.05])
                    else:
                        equipText = infoButtonsFont.render("Equip", 1, (255, 255, 255))
                        equipButton = pg.draw.rect(inventorySurface, (85, 85, 85, 230),[WIDTH * 0.8025, HEIGHT * 0.71, WIDTH * 0.08, HEIGHT * 0.05])
                    equipRect = equipText.get_rect()
                    equipRect.midtop = (WIDTH * 0.8425, HEIGHT * 0.71)
                    inventorySurface.blit(equipText, equipRect)
                    if mouseclicked and equipButton.collidepoint(mousePos):
                        if equipped == selectedItem.itemid:
                            equipped = -1
                        else:
                            equipped = selectedItem.itemid










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
