import pygame as pg
import sys

from booboom.map import Map
from booboom.object_handler import ObjectHandler
from booboom.object_renderer import ObjectRenderer
from booboom.pathfinding import PathFinding
from booboom.player import Player
from booboom.raycasting import RayCasting
from booboom.settings import *
from booboom.sound import Sound
from booboom.weapon import Weapon


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT
        pg.time.set_timer(self.global_event, 40)
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.path_finding = PathFinding(self)

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.path_finding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption("{:.1f}".format(self.clock.get_fps()))

    def draw(self):
        if DEBUG_DRAW_MAP or DEBUG_DRAW_PLAYER_CIRCLE or DEBUG_DRAW_PLAYER_MOVEMENT or DEBUG_DRAW_RAYCASTING_LINES:
            self.screen.fill("black")
        self.object_renderer.draw()
        self.weapon.draw()
        self.map.draw()
        self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
