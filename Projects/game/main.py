import pygame as pg
import random
import math

import Item
from inventory import inventory
from object import *
from copy import copy
import recipe

WIDTH = 1000
HEIGHT = 600
fps = 60
middle = pg.Vector2(WIDTH / 2, HEIGHT / 2)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Something')
overlaySurface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

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
inventorySelected = -1
equipped = -1
descriptionHeight = 0

craftingActive = False
craftingSelected = -1
craftingInventory = [[None, None, None], [None, None, None], [None, None, None]]



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

def createObject(object, loc=None):
    if isinstance(object, objectEnum):
        if loc is None:
            newPos = randomPos()
            objectList.append(Object(object, newPos))
        else:
            objectList.append(Object(object, pg.Vector2(loc)))

def draw_text(screen_object, font, string, loc, color):
    text = font.render(string, True, color)
    text_rect = text.get_rect()
    text_rect.center = loc
    screen_object.blit(text, text_rect)
    return text_rect.height

#start function
def start():
    for i in range(500):
        choice = random.choices([objectEnum.STONE, objectEnum.IRON, objectEnum.GOLD], [10, 4, 1])
        createObject(choice[0])
    createObject(objectEnum.TREE, (0, 0))
    createObject(objectEnum.TREE, (50, 0))
    inventory.add(Item.item('Iron Pick', 1, "sprites/items/pickaxe.png", ItemType.Tool, "Isn't it Iron Pick?\nI'm gonna kill myself", 100, 10))

def checkInventoryEmpty():
    for row in craftingInventory:
        for item in row:
            if not item is None:
                return False
    return True

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
    global craftingActive
    global vel
    global pos
    global pickaxeAngle
    global swinging
    global swingingDown
    global mouseAngle
    global inventorySelected
    global craftingSelected
    global descriptionHeight
    global equipped
    global craftingInventory

    keys = pg.key.get_pressed()

    acc = pg.Vector2(0, 0)
    # movement
    if not (inventoryActive or craftingActive):
        if keys[pg.K_w]:
            acc.y -= moveAccMag
        if keys[pg.K_s]:
            acc.y += moveAccMag
        if keys[pg.K_a]:
            acc.x -= moveAccMag
        if keys[pg.K_d]:
            acc.x += moveAccMag


    vel += acc

    if not (inventoryActive or craftingActive):
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

    if not (inventoryActive or craftingActive):
        mouseAngle = math.radians(180 - angleBetween(middle, pg.Vector2(mousePos[0], mousePos[1])))

    pg.draw.rect(screen, (50, 50, 50), [WIDTH * 0.58 - pos.x, HEIGHT * -1.035 - pos.y, WIDTH * 3.04, HEIGHT * 3.07])
    pg.draw.rect(screen, (92, 70, 41), [WIDTH * 0.6 - pos.x, HEIGHT * -1 - pos.y, WIDTH * 3, HEIGHT * 3])


    armSurface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    pg.draw.rect(armSurface, 'white', [middle.x, middle.y + 5, 20, 5])

    if swinging and not (inventoryActive or craftingActive):
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
            pg.draw.line(armSurface, (0, 0, 0), (middle.x + 20, middle.y + 7.5),(middle.x + 20 + stickPos, middle.y + 7.5), 2)
            pg.draw.line(armSurface, (0, 0, 0), (middle.x + 20 + startPos, middle.y + 7.5),(middle.x + 20 + endPos, middle.y + 7.5), 3)
    else:
        pg.draw.rect(armSurface, 'white', [middle.x + 15, middle.y + 5, stickPos, 5])

    armSurface, rect = rotate_on_pivot(armSurface, math.degrees(mouseAngle), middle, middle)

    screen.blit(armSurface, rect)

    pg.draw.circle(screen, 'white', middle, 10)

    #mouse click
    mouseclicked = [False, False]
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                mouseclicked[0] = True
            if event.button == pg.BUTTON_RIGHT:
                mouseclicked[1] = True

    for object in objectList:
        objectPosition = object.position
        if isinstance(objectPosition, pg.Vector2):
            distance = middle.distance_to(objectPosition - pos)
            if distance <= reach:
                image = object.display(1, screen, object.position - pos - object.offset)
                pg.draw.rect(screen, (255, 0, 0), [objectPosition - pos - pg.Vector2(17, 25) - object.bar_offset, pg.Vector2(34, 5)])
                pg.draw.rect(screen, (0, 255, 0), [objectPosition - pos - pg.Vector2(17, 25) - object.bar_offset, pg.Vector2(34 * (object.health / object.max_health), 5)])
                if pg.mouse.get_pressed(3)[0] and not inventoryActive:
                    if image.collidepoint(mousePos):
                        if not swinging:
                            swinging = True
                            if equipped != -1:
                                equippedItem = inventory.find(equipped)
                                if isinstance(equippedItem, Item.item):
                                    object.health -= equippedItem.damage
                            else:
                                object.health -= 0.5
                            object.flashTick = objectFlashLength
                            if object.health <= 0:
                                equippedItem = inventory.find(equipped)
                                if isinstance(equippedItem, Item.item):
                                    equippedItem.durability -= 1
                                    if equippedItem.durability <= 0:
                                        inventory.remove(equippedItem)
                                        equipped = -1
                                newPos = randomPos()
                                object.position = newPos
                                object.health = object.max_health
                                object.flashTick = 0
                                if isinstance(object.dropItem, Item.item):
                                    inventory.add(object.dropItem)
        if object.flashTick > 0:
            object.flashTick -= 1
            object.display(2, screen, object.position - pos - object.offset)
        else:
            object.display(0, screen, object.position - pos - object.offset)




    #inventory
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                if inventoryActive:
                    inventoryActive = False
                    inventorySelected = -1
                else:
                    if craftingActive:
                        craftingActive = False
                        craftingSelected = -1
                        for row in craftingInventory:
                            for item in row:
                                if item != None:
                                    inventory.add(item)
                        craftingInventory = [[None, None, None], [None, None, None], [None, None, None]]
                        craftingSelected = -1
                    inventoryActive = True
            if event.key == pg.K_c:
                if craftingActive:
                    craftingActive = False
                    craftingSelected = -1
                    for row in craftingInventory:
                        for item in row:
                            if item != None:
                                inventory.add(item)
                    craftingInventory = [[None, None, None], [None, None, None], [None, None, None]]
                    craftingSelected = -1
                else:
                    if inventoryActive:
                        inventoryActive = False
                        inventorySelected = -1
                    craftingActive = True

    if inventoryActive:
        pg.draw.rect(overlaySurface, (200, 200, 200, 230), [WIDTH * 0.05, HEIGHT * 0.1, WIDTH * 0.9, HEIGHT * 0.72]) # inventory background

        sort_button = pg.draw.rect(overlaySurface, (85, 85, 85, 230), [WIDTH * 0.645, HEIGHT * 0.105, WIDTH * 0.06, HEIGHT * 0.035]) # sort method button

        if mouseclicked[0] and sort_button.collidepoint(mousePos):
            if inventory.sortingType == "Name":
                inventory.sortingType = "Count"
            else:
                inventory.sortingType = "Name"
            inventorySelected = -1

        draw_text(overlaySurface, sortFont, inventory.sortingType,(WIDTH * 0.675, HEIGHT * 0.1225), (255, 255, 255))

        if mouseclicked[0] and pg.Rect([WIDTH * 0.714, HEIGHT * 0.105, WIDTH * 0.021, HEIGHT * 0.035]).collidepoint(mousePos):
            if inventory.sortDown:
                inventory.sortDown = False
            else:
                inventory.sortDown = True
            inventorySelected = -1

        pg.draw.rect(overlaySurface, (85, 85, 85, 230), [WIDTH * 0.714, HEIGHT * 0.105, WIDTH * 0.021, HEIGHT * 0.035]) # sort direction button
        if inventory.sortDown:
            pg.draw.polygon(overlaySurface, (255, 255, 255, 255), [(WIDTH * 0.734, HEIGHT *  0.114275), (WIDTH * 0.7245, HEIGHT *  0.130725), (WIDTH * 0.715, HEIGHT *  0.114275)], 1)
        else:
            pg.draw.polygon(overlaySurface, (255, 255, 255, 255),[(WIDTH * 0.734, HEIGHT * 0.130725), (WIDTH * 0.7245, HEIGHT * 0.114275), (WIDTH * 0.715, HEIGHT * 0.130725)], 1)


        for i in range(4):
            for j in range(7):
                index = 7 * i + j
                if index == inventorySelected:
                    pg.draw.rect(overlaySurface, (100, 100, 100, 230), [WIDTH * 0.07 + WIDTH * 0.095 * j, HEIGHT * 0.135 + HEIGHT * 0.16 * i, WIDTH * 0.1, HEIGHT * 0.17])
                slot = pg.draw.rect(overlaySurface, (150, 150, 150, 230), [WIDTH * 0.075 + WIDTH * 0.095 * j, HEIGHT * 0.145 + HEIGHT * 0.16 * i, WIDTH * 0.09, HEIGHT * 0.15]) # inventory slots
                if mouseclicked[0] and slot.collidepoint(mousePos):
                    if index < len(inventory.items):
                        inventorySelected = index

        for i, item in enumerate(inventory.items):
            x = i % 9
            y = i // 9

            item.display(overlaySurface, (WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.145 + HEIGHT * 0.16 * y), (WIDTH * 0.09, HEIGHT * 0.15))

            pg.draw.rect(overlaySurface, (220, 220, 220, 230), [WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.265 + HEIGHT * 0.16 * y, WIDTH * 0.09, HEIGHT * 0.03]) # item name background

            draw_text(overlaySurface, nameFont, item.name, (WIDTH * 0.12 + WIDTH * 0.095 * x, HEIGHT * 0.28 + HEIGHT * 0.16 * y), (0, 0, 0))

            if item.type == ItemType.Material:
                pg.draw.rect(overlaySurface, (220, 220, 220, 230),[WIDTH * 0.075 + WIDTH * 0.095 * x, HEIGHT * 0.145 + HEIGHT * 0.16 * y, WIDTH * 0.02,HEIGHT * 0.034])  # item count background
                draw_text(overlaySurface, countFont, str(item.count), (WIDTH * 0.085 + WIDTH * 0.095 * x, HEIGHT * 0.162 + HEIGHT * 0.16 * y), (0, 0, 0))
            if item.type == ItemType.Tool:
                durability_percentage = item.durability / item.max_durability
                pg.draw.rect(overlaySurface, (100, 100, 100, 230), [WIDTH * 0.084 + WIDTH * 0.095 * x, HEIGHT * 0.25 + HEIGHT * 0.16 * y, WIDTH * 0.072,HEIGHT * 0.01])
                pg.draw.rect(overlaySurface, (200, 200, 200, 230),[WIDTH * 0.0858 + WIDTH * 0.095 * x, HEIGHT * 0.252 + HEIGHT * 0.16 * y, WIDTH * 0.0702 * durability_percentage, HEIGHT * 0.0069])

        pg.draw.rect(overlaySurface, (180, 180, 180, 230), [WIDTH * 0.75, HEIGHT * 0.145, WIDTH * 0.185, HEIGHT * 0.63])

        pg.draw.rect(overlaySurface, (160, 160, 160, 230),[WIDTH * 0.76, HEIGHT * 0.16, WIDTH * 0.165, HEIGHT * 0.04]) # item name
        pg.draw.rect(overlaySurface, (160, 160, 160, 230),[WIDTH * 0.76, HEIGHT * 0.21, WIDTH * 0.165, HEIGHT * 0.27]) # item visual
        pg.draw.rect(overlaySurface, (160, 160, 160, 230),[WIDTH * 0.76, HEIGHT * 0.49, WIDTH * 0.165, descriptionHeight + HEIGHT * .02]) # item description

        if inventorySelected != -1:
            selectedItem = inventory.items[inventorySelected]
            if isinstance(selectedItem, Item.item):
                draw_text(overlaySurface, infoNameFont, selectedItem.name, (WIDTH * 0.8425, HEIGHT * 0.18), (0, 0, 0))

                selectedItem.display(overlaySurface, (WIDTH * 0.76, HEIGHT * 0.21), (WIDTH * 0.165, HEIGHT * 0.27))

                lineList = selectedItem.description.split('\n')
                totalHeight = 0
                for line in lineList:
                    totalHeight += draw_text(overlaySurface, infoDescriptionFont, line, (WIDTH * 0.8425, HEIGHT * 0.515 + totalHeight), (0, 0, 0))
                descriptionHeight = totalHeight

                if selectedItem.type == ItemType.Tool:
                    pg.draw.rect(overlaySurface, (160, 160, 160, 230), [WIDTH * 0.76, HEIGHT * 0.52 + descriptionHeight, WIDTH * 0.165, HEIGHT * .085])  # item info
                    draw_text(overlaySurface, infoDescriptionFont, f"Durability: {selectedItem.durability} / {selectedItem.max_durability}", (WIDTH * 0.8425, HEIGHT * 0.545 + descriptionHeight), (0, 0, 0))
                    draw_text(overlaySurface, infoDescriptionFont, f"Damage: {selectedItem.damage}", (WIDTH * 0.8425, HEIGHT * 0.575 + descriptionHeight), (0, 0, 0))

                    if equipped == selectedItem.itemid:
                        equipText = "Unequip"
                        equipButton = pg.draw.rect(overlaySurface, (85, 85, 85, 230),[WIDTH * 0.7925, HEIGHT * 0.71, WIDTH * 0.1, HEIGHT * 0.05])
                    else:
                        equipText = "Equip"
                        equipButton = pg.draw.rect(overlaySurface, (85, 85, 85, 230),[WIDTH * 0.8025, HEIGHT * 0.71, WIDTH * 0.08, HEIGHT * 0.05])
                    draw_text(overlaySurface, infoButtonsFont, equipText, (WIDTH * 0.8425, HEIGHT * 0.735), (255, 255, 255))
                    if mouseclicked[0] and equipButton.collidepoint(mousePos):
                        if equipped == selectedItem.itemid:
                            equipped = -1
                        else:
                            equipped = selectedItem.itemid

    if craftingActive:
        pg.draw.rect(overlaySurface, (200, 200, 200, 230), [WIDTH * 0.025, HEIGHT * 0.1, WIDTH * 0.95, HEIGHT * 0.72]) # crafting background

        sort_button = pg.draw.rect(overlaySurface, (85, 85, 85, 230), [WIDTH * 0.62, HEIGHT * 0.105, WIDTH * 0.06, HEIGHT * 0.035])  # sort method button

        if mouseclicked[0] and sort_button.collidepoint(mousePos):
            if inventory.sortingType == "Name":
                inventory.sortingType = "Count"
            else:
                inventory.sortingType = "Name"
            craftingSelected = -1

        draw_text(overlaySurface, sortFont, inventory.sortingType, (WIDTH * 0.65, HEIGHT * 0.1220), (255, 255, 255))

        if mouseclicked[0] and pg.Rect([WIDTH * 0.689, HEIGHT * 0.105, WIDTH * 0.021, HEIGHT * 0.035]).collidepoint(
                mousePos):
            if inventory.sortDown:
                inventory.sortDown = False
            else:
                inventory.sortDown = True
            craftingSelected = -1

        pg.draw.rect(overlaySurface, (85, 85, 85, 230),[WIDTH * 0.689, HEIGHT * 0.105, WIDTH * 0.021, HEIGHT * 0.035])  # sort direction button
        if inventory.sortDown:
            pg.draw.polygon(overlaySurface, (255, 255, 255, 255),[(WIDTH * 0.709, HEIGHT * 0.114275), (WIDTH * 0.6995, HEIGHT * 0.130725), (WIDTH * 0.690, HEIGHT * 0.114275)], 1)
        else:
            pg.draw.polygon(overlaySurface, (255, 255, 255, 255),[(WIDTH * 0.709, HEIGHT * 0.130725), (WIDTH * 0.6995, HEIGHT * 0.114275), (WIDTH * 0.690, HEIGHT * 0.130725)], 1)

        for i in range(4):
            for j in range(7):
                index = 7 * i + j
                if index == craftingSelected:
                    pg.draw.rect(overlaySurface, (100, 100, 100, 230),[WIDTH * 0.045 + WIDTH * 0.095 * j, HEIGHT * 0.135 + HEIGHT * 0.16 * i, WIDTH * 0.1, HEIGHT * 0.17])
                slot = pg.draw.rect(overlaySurface, (150, 150, 150, 230),[WIDTH * 0.05 + WIDTH * 0.095 * j, HEIGHT * 0.145 + HEIGHT * 0.16 * i, WIDTH * 0.09, HEIGHT * 0.15])  # inventory slots
                if mouseclicked[0] and slot.collidepoint(mousePos):
                    if index < len(inventory.items):
                        craftingSelected = index

        for i, item in enumerate(inventory.items):
            x = i % 9
            y = i // 9

            item.display(overlaySurface, (WIDTH * 0.05 + WIDTH * 0.095 * x, HEIGHT * 0.145 + HEIGHT * 0.16 * y), (WIDTH * 0.09, HEIGHT * 0.15))

            pg.draw.rect(overlaySurface, (220, 220, 220, 230), [WIDTH * 0.05 + WIDTH * 0.095 * x, HEIGHT * 0.265 + HEIGHT * 0.16 * y, WIDTH * 0.09, HEIGHT * 0.03]) # item name background

            draw_text(overlaySurface, nameFont, item.name, (WIDTH * 0.095 + WIDTH * 0.095 * x, HEIGHT * 0.28 + HEIGHT * 0.16 * y), (0, 0, 0))

            if item.type == ItemType.Material:
                pg.draw.rect(overlaySurface, (220, 220, 220, 230),[WIDTH * 0.05 + WIDTH * 0.095 * x, HEIGHT * 0.145 + HEIGHT * 0.16 * y, WIDTH * 0.02,HEIGHT * 0.034])  # item count background

                draw_text(overlaySurface, countFont, str(item.count), (WIDTH * 0.06 + WIDTH * 0.095 * x, HEIGHT * 0.162 + HEIGHT * 0.16 * y), (0, 0, 0))
            if item.type == ItemType.Tool:
                durability_percentage = item.durability / item.max_durability
                pg.draw.rect(overlaySurface, (100, 100, 100, 230), [WIDTH * 0.059 + WIDTH * 0.095 * x, HEIGHT * 0.25 + HEIGHT * 0.16 * y, WIDTH * 0.072,HEIGHT * 0.01])
                pg.draw.rect(overlaySurface, (200, 200, 200, 230),[WIDTH * 0.0608 + WIDTH * 0.095 * x, HEIGHT * 0.252 + HEIGHT * 0.16 * y, WIDTH * 0.0702 * durability_percentage, HEIGHT * 0.0069])

        for i in range(3):
            for j in range(3):
                slot = pg.draw.rect(overlaySurface, (150, 150, 150, 230), [WIDTH * 0.729 + WIDTH * 0.077 * j, HEIGHT * 0.145 + HEIGHT * 0.13 * i, WIDTH * 0.072, HEIGHT * 0.12])
                craftingItem = craftingInventory[i][j]
                if craftingItem != None:
                    craftingItem.display(overlaySurface, (WIDTH * 0.729 + WIDTH * 0.077 * j, HEIGHT * 0.145 + HEIGHT * 0.13 * i), (WIDTH * 0.072, HEIGHT * 0.12))
                if slot.collidepoint(mousePos):
                    if mouseclicked[0] and craftingSelected != -1 and craftingInventory[i][j] is None:
                        selectedItem = inventory.items[craftingSelected]
                        if selectedItem.type == ItemType.Tool:
                            inventory.remove(selectedItem)
                            craftingSelected = -1
                            craftingInventory[i][j] = selectedItem
                        else:
                            itemCopy = copy(selectedItem)
                            itemCopy.count = 1
                            if selectedItem.count == 1:
                                craftingSelected = -1
                            inventory.remove(itemCopy)
                            craftingInventory[i][j] = itemCopy
                    if mouseclicked[1] and craftingInventory[i][j] is not None:
                        inventory.add(craftingInventory[i][j])
                        craftingInventory[i][j] = None

        pg.draw.rect(overlaySurface, (150, 150, 150, 230), [WIDTH * 0.798, HEIGHT * 0.535, WIDTH * 0.09, HEIGHT * 0.15])
        if not checkInventoryEmpty():
            clear_button = pg.draw.rect(overlaySurface, (85, 85, 85, 230), [WIDTH * 0.883, HEIGHT * 0.105, WIDTH * 0.072, HEIGHT * 0.035]) # clear
            draw_text(overlaySurface, sortFont, "Clear", (WIDTH * 0.919, HEIGHT * 0.1220), (255, 255, 255))
            if mouseclicked[0] and clear_button.collidepoint(mousePos):
                for row in craftingInventory:
                    for item in row:
                        if item != None:
                            inventory.add(item)
                craftingInventory = [[None, None, None], [None, None, None], [None, None, None]]
                craftingSelected = -1

            recipeOutput = recipe.checkRecipes([craftingInventory])
            if not recipeOutput is None:
                craft_button = pg.draw.rect(overlaySurface, (85, 85, 85, 230),[WIDTH * 0.806, HEIGHT * 0.695, WIDTH * 0.072, HEIGHT * 0.035])  # craft
                draw_text(overlaySurface, sortFont, "Craft", (WIDTH * 0.842, HEIGHT * 0.712), (255, 255, 255))
                recipeOutput.display(overlaySurface, (WIDTH * 0.798, HEIGHT * 0.535), (WIDTH * 0.09, HEIGHT * 0.15))
                if mouseclicked[0] and craft_button.collidepoint(mousePos):
                    craftingInventory = [[None, None, None], [None, None, None], [None, None, None]]
                    craftingSelected = -1
                    inventory.add(recipeOutput)











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
    overlaySurface.fill((255, 255, 255, 0))

    update(events)

    screen.blit(overlaySurface, (0, 0))


    pg.display.flip()

    clock.tick(fps)
