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
difference_acceptance = math.radians(9) # degrees of freedom for scoring
score = 0

#menu variables
playing = False


#colors
background_color = pg.Color(79, 85, 182)
lock_color = pg.Color(7, 6, 54)
shackle_color = pg.Color(49, 49, 96)
line_color = pg.Color(185, 16, 75)
target_color = pg.Color(240, 207, 76)
score_color = pg.Color(200, 201, 220)

menu_button_color = pg.Color(62, 169, 241)
menu_button_shadow_color = pg.Color(22, 64, 93)
menu_button_hover_color = pg.Color(124, 195, 243)
menu_button_text_color = pg.Color(203, 224, 239)
menu_button_interact_text_color = pg.Color(116, 155, 182)
menu_button_interact_color = pg.Color(157, 207, 241)
title_color = pg.Color(153, 109, 212)
title_shadow_color = pg.Color(127, 78, 192)

#visual variables
lock_radius = 100
lock_thickness = 25

shackle_height = 125
shackle_thickness = 25
shackle_radius = 50

#fonts
score_font = pg.font.Font("assets/grobold.ttf", 40)
title_font = pg.font.Font("assets/grobold.ttf", 60)
button_font = pg.font.Font("assets/grobold.ttf", 40)


class Button:
    def __init__(self, x, y, w, h, z, text, button_color, shadow_color, hover_color, interact_color, text_color, interact_text_color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.z = z
        self.text = text
        self.button_color = button_color
        self.shadow_color = shadow_color
        self.hover_color = hover_color
        self.interact_color = interact_color
        self.text_color = text_color
        self.interact_text_color = interact_text_color
        self.was_down_last_frame = False

    def draw(self, surface):
        mouse_pos = pg.mouse.get_pos()
        mouse_down = pg.mouse.get_pressed()[0]
        if pg.Rect(self.x, self.y, self.w, self.h).collidepoint(mouse_pos[0], mouse_pos[1]):
            if mouse_down:
                pg.draw.rect(surface, self.interact_color, pg.Rect(self.x, self.y + self.z, self.w, self.h), border_radius=12)
                draw_text(surface, button_font, self.text, self.interact_text_color, pg.Vector2(self.x + self.w / 2, self.y + self.h / 2 + self.z))
                self.was_down_last_frame = True
            else:
                pg.draw.rect(surface, self.shadow_color, pg.Rect(self.x, self.y + self.z, self.w, self.h), border_radius=12)
                pg.draw.rect(surface, self.hover_color, pg.Rect(self.x, self.y, self.w, self.h), border_radius=12)
                draw_text(surface, button_font, self.text, self.text_color, pg.Vector2(self.x + self.w / 2, self.y + self.h / 2))
                if self.was_down_last_frame:
                    self.was_down_last_frame = False
                    return True
        else:
            pg.draw.rect(surface, self.shadow_color, pg.Rect(self.x, self.y + self.z, self.w, self.h), border_radius=12)
            pg.draw.rect(surface, self.button_color, pg.Rect(self.x, self.y, self.w, self.h), border_radius=12)
            draw_text(surface, button_font, self.text, self.text_color, pg.Vector2(self.x + self.w / 2, self.y + self.h / 2))
            if self.was_down_last_frame:
                self.was_down_last_frame = False
                return True
        return False

#buttons
start_button = Button(200, 250, 200, 50, 10, "Start", menu_button_color, menu_button_shadow_color, menu_button_hover_color, menu_button_interact_color, menu_button_text_color, menu_button_interact_text_color)

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
    global playing

    global line_angle
    global line_speed
    global line_direction
    global target_angle
    global score


    if playing:
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
    else:
        draw_text(screen, title_font, "(Not) Pop the Lock", title_shadow_color, MIDDLE + pg.Vector2(0, -190))
        draw_text(screen, title_font, "(Not) Pop the Lock", title_color, MIDDLE + pg.Vector2(0, -200))

        released = start_button.draw(screen)
        if released:
            playing = True

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