import typing

import pygame as pg

from booboom.settings import *
if typing.TYPE_CHECKING:
    from booboom.main import Game


_ = False
map_source = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1],
]


class Map:
    def __init__(self, game: "Game"):
        self.game = game
        self.map_source = map_source
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.map_source):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        if DEBUG_DRAW_MAP:
            [pg.draw.rect(self.game.screen, "darkgray", (pos[0] * 100, pos[1] * 100, 100, 100), 2) for pos in self.world_map]

    @property
    def cols(self):
        return len(self.map_source[0])

    @property
    def rows(self):
        return len(self.map_source)
