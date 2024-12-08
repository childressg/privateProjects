import math
import random

import pygame as pg

WIDTH, HEIGHT = 600, 600
MIDDLE = pg.Vector2(WIDTH / 2, HEIGHT / 2)
FPS = 60

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.NOFRAME)
pg.display.set_caption('pop the lock')

clock = pg.time.Clock()
running = True

#gameplay variables
line_angle = 0
line_speed = 0.02
line_direction = 1
target_angle = math.radians(random.randrange(0, 360))
difference_acceptance = math.radians(10) # degrees of freedom for scoring
score = 0

#colors
background_color = pg.Color(79, 85, 182)
lock_color = pg.Color(7, 6, 54)
shackle_color = pg.Color(49, 49, 96)
line_color = pg.Color(185, 16, 75)
target_color = pg.Color(240, 207, 76)
score_color = pg.Color(200, 201, 220)

#visual variables
lock_radius = 100
lock_thickness = 25

shackle_height = 125
shackle_thickness = 25
shackle_radius = 50

#fonts
score_font = pg.font.Font("assets/grobold.ttf", 40)

def draw_rounded_line(surface, color, start_pos, end_pos, width):
    pg.draw.line(surface, color, start_pos, end_pos, width)
    pg.draw.circle(surface, color, start_pos, width / 2)
    pg.draw.circle(surface, color, end_pos, width / 2)

def draw_text(surface, font, text, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = center
    surface.blit(text_surface, text_rect)

def check_angle():
    return abs(line_angle - target_angle) < difference_acceptance or abs((line_angle - math.pi * 2) - target_angle) < difference_acceptance or abs((line_angle + math.pi * 2) - target_angle) < difference_acceptance

def start():
    pass

def update(events):
    global line_angle
    global line_speed
    global line_direction
    global target_angle
    global score

    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # print(line_angle - target_angle, difference_acceptance)
                if check_angle():
                    line_direction *= -1
                    line_speed += 0.001
                    target_angle = math.radians(random.randrange(0, 360))
                    score += 1
    #shackle
    pg.draw.circle(screen, shackle_color, MIDDLE - pg.Vector2(0, shackle_height), shackle_radius)
    pg.draw.circle(screen, background_color, MIDDLE - pg.Vector2(0, shackle_height), shackle_radius - shackle_thickness)
    pg.draw.rect(screen, shackle_color, pg.Rect(MIDDLE.x - shackle_radius, MIDDLE.y - shackle_height, 2 * shackle_radius, shackle_height))
    pg.draw.rect(screen, background_color, pg.Rect(MIDDLE.x - (shackle_radius - shackle_thickness), MIDDLE.y - shackle_height, 2 * (shackle_radius - shackle_thickness), shackle_height))
    pg.draw.circle(screen, background_color, MIDDLE, lock_radius - lock_thickness)

    #lock
    draw_text(screen, score_font, str(score), score_color, MIDDLE)
    pg.draw.circle(screen, lock_color, MIDDLE, lock_radius, lock_thickness)

    #gameplay
    pg.draw.circle(screen, target_color, MIDDLE + pg.Vector2(((lock_radius + (lock_radius - lock_thickness)) / 2) * math.cos(target_angle),-((lock_radius + (lock_radius - lock_thickness)) / 2) * math.sin(target_angle)), lock_thickness * .40)
    draw_rounded_line(screen, line_color, MIDDLE + pg.Vector2((lock_radius - lock_thickness + 5) * math.cos(line_angle), -(lock_radius - lock_thickness + 5) * math.sin(line_angle)), MIDDLE + pg.Vector2((lock_radius - 5) * math.cos(line_angle), -(lock_radius - 5) * math.sin(line_angle)), 8)
    #debug lines
    # pg.draw.line(screen, (255, 255, 255), MIDDLE + pg.Vector2((lock_radius - lock_thickness) * math.cos(target_angle + difference_acceptance), -(lock_radius - lock_thickness) * math.sin(target_angle + difference_acceptance)), MIDDLE + pg.Vector2(lock_radius * math.cos(target_angle + difference_acceptance), -lock_radius * math.sin(target_angle + difference_acceptance)))
    # pg.draw.line(screen, (255, 255, 255), MIDDLE + pg.Vector2((lock_radius - lock_thickness) * math.cos(target_angle - difference_acceptance), -(lock_radius - lock_thickness) * math.sin(target_angle - difference_acceptance)), MIDDLE + pg.Vector2(lock_radius * math.cos(target_angle - difference_acceptance), -lock_radius * math.sin(target_angle - difference_acceptance)))

    line_angle += line_speed * line_direction
    line_angle = line_angle % (math.pi * 2)

start()

while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    screen.fill(background_color)
    update(events)
    pg.display.flip()
    clock.tick(FPS)

pg.quit()