from collections import deque
import importlib.resources
import os
import typing

import pygame as pg

from booboom.settings import *
if typing.TYPE_CHECKING:
    from booboom.main import Game


class SpriteObject:
    def __init__(self, game: "Game", file_path: str, pos: tuple[float, float], scale: 1.0, shift: 0.0):
        self.game = game
        self.player = game.player
        self.sprite_scale = scale
        self.sprite_height_shift = shift
        self.x, self.y = pos
        self.image_width = 0
        self.image_half_width = 0
        self.image_ratio = 0.0
        self.image = self.load_image(file_path)
        self.dx, self.dy = 0.0, 0.0
        self.theta = 0.0
        self.screen_x = 0.0
        self.dist = 1.0
        self.norm_dist = 1.0
        self.sprite_half_width = 0.0

    def load_image(self, file_path: str):
        with (importlib.resources.files("booboom") / "resources" / RESOURCE_SET / "sprites" / file_path).open("rb") as f:
            image = pg.image.load(f).convert_alpha()
        self.image_width = image.get_width()
        self.image_half_width = self.image_width // 2
        self.image_ratio = self.image_width / image.get_height()
        return image

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.sprite_scale
        proj_width, proj_height = proj * self.image_ratio, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.sprite_height_shift
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.pi * 2

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.image_half_width < self.screen_x < (WIDTH + self.image_half_width) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game: "Game", dir_path: str, pos: tuple[float, float], scale=1.0, shift=0.0, animation_time=120):
        self.dir_obj = importlib.resources.files("booboom") / "resources" / RESOURCE_SET / "sprites" / dir_path
        self.images = self.get_images(self.dir_obj)
        file_path = os.path.join(dir_path, sorted(x.name for x in self.dir_obj.iterdir() if x.is_file())[0])
        super().__init__(game=game, file_path=file_path, pos=pos, scale=scale, shift=shift)
        self.animation_time = animation_time
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, dir_obj):
        images = deque()
        for file_name in sorted(x.name for x in dir_obj.iterdir() if x.is_file()):
            with (dir_obj / file_name).open("rb") as f:
                img = pg.image.load(f).convert_alpha()
            images.append(img)

        return images
