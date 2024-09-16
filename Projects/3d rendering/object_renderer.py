import pygame as pg
from settings import *


def darken(c, p):
    return int(c[0] * ((100 - p) / 100)), int(c[1] * ((100 - p) / 100)), int(c[2] * ((100 - p) / 100))


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        gradient_height = HALF_HEIGHT // GRADIENT_COUNT
        for i in range(GRADIENT_COUNT):
            pg.draw.rect(self.screen, darken(CEILING_COLOR, i * GRADIENT_STRENGTH), (0, i * gradient_height, WIDTH, gradient_height)) # ceiling
        for i in range(GRADIENT_COUNT):
            pg.draw.rect(self.screen, darken(FLOOR_COLOR, i * GRADIENT_STRENGTH), (0, HEIGHT - gradient_height * (i + 1) , WIDTH, gradient_height)) # floor

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos, shadow in list_objects:
            self.screen.blit(image, pos)
            if shadow:
                darkness = pg.Surface(image.get_size()).convert_alpha()
                darkness.fill((0, 0, 0, min(depth * 10, 255)))
                self.screen.blit(darkness, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/wall.png')
        }