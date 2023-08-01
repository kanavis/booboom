import importlib.resources
import typing

import pygame as pg

from booboom.settings import *

if typing.TYPE_CHECKING:
    from booboom.main import Game


class Sound:
    def __init__(self, game: "Game"):
        self.game = game
        pg.mixer.init()
        self.shotgun_shot = self.load_sound("shotgun_shot.mp3")
        self.mob1_hit = self.load_sound("mob1_hit.mp3")
        self.mob1_death = self.load_sound("mob1_death.mp3")
        self.mob1_shot = self.load_sound("mob1_shot.mp3")
        self.player_hit = self.load_sound("player_hit.mp3")
        self.player_death = self.load_sound("player_death.mp3")
        self.win = self.load_sound("win.mp3")

    def load_sound(self, name: str):
        with (importlib.resources.files("booboom") / "resources" / RESOURCE_SET / "sounds" / name).open("rb") as f:
            return pg.mixer.Sound(f)
