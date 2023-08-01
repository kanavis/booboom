import importlib.resources
import typing

import pygame as pg

from booboom.settings import *
if typing.TYPE_CHECKING:
    from booboom.main import Game


class ObjectRenderer:
    def __init__(self, game: "Game"):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture("textures/sky.png", (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture("textures/blood_screen.png", RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f"textures/digits/{i}.png", (self.digit_size, self.digit_size)) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture("textures/game_over.png", RES)
        self.win_image = self.get_texture("textures/win.png", RES)

    def draw(self):
        if DRAW_3D:
            self.draw_background()
            self.render_game_objects()
            self.draw_player_health()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def draw_player_health(self):
        if self.game.player.health <= 0:
            return
        health = str(self.game.player.health)
        i = -1
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits["10"], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    def get_texture(self, resource_file, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        with (importlib.resources.files("booboom") / "resources" / RESOURCE_SET / resource_file).open("rb") as f:
            texture = pg.image.load(f).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {x: self.get_texture("textures/wall_{}.png".format(x)) for x in range(1, 5)}
