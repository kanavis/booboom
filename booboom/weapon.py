import typing
from collections import deque

import pygame as pg

from booboom.settings import *
from booboom.sprite_object import AnimatedSprite

if typing.TYPE_CHECKING:
    from booboom.main import Game


class Weapon(AnimatedSprite):
    def __init__(self, game: "Game", dir_path="weapon/shotgun", scale=0.7, animation_time=90, damage=50):
        super().__init__(game=game, dir_path=dir_path, pos=(0, 0), scale=scale, animation_time=animation_time)
        self.images = deque(
            pg.transform.scale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
            for img in self.images
        )
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = damage

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
