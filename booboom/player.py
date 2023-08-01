import typing

import pygame as pg

from booboom.settings import *
if typing.TYPE_CHECKING:
    from booboom.main import Game


class Player:
    def __init__(self, game: "Game"):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.rel = 0
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 900
        self.health_recovery_hit_delay = 1500
        self.time_prev = pg.time.get_ticks()
        self.last_attack = pg.time.get_ticks()

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if (
            time_now - self.time_prev >= self.health_recovery_delay and
            time_now - self.last_attack >= self.health_recovery_hit_delay
        ):
            self.time_prev = time_now
            return True
        return False

    def check_game_over(self):
        if self.health <= 0:
            self.game.sound.player_death.play()
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(3000)
            self.game.new_game()

    def get_damage(self, damage):
        self.last_attack = pg.time.get_ticks()
        self.health -= damage
        self.game.sound.player_hit.play()
        self.game.object_renderer.player_damage()
        self.check_game_over()

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun_shot.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = PLAYER_SPEED * self.game.delta_time
        speed_cos = speed * cos_a
        speed_sin = speed * sin_a
        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        self.move_if_available(dx, dy)

        self.angle %= math.pi * 2

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def move_if_available(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        moved = False
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
            moved = True
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
            moved = True
        if moved:
            self.check_win()

    def check_win(self):
        if self.game.object_handler.portal_tile is not None and self.map_pos == self.game.object_handler.portal_tile:
            self.game.sound.win.play()
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(3000)
            self.game.new_game()

    def draw(self):
        if DEBUG_DRAW_PLAYER_MOVEMENT:
            pg.draw.line(
                self.game.screen,
                "yellow",
                (self.x * 100, self.y * 100),
                (
                    self.x * 100 + WIDTH * math.cos(self.angle),
                    self.y * 100 + WIDTH * math.sin(self.angle),
                ),
                2,
            )
        if DEBUG_DRAW_PLAYER_CIRCLE:
            pg.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_LEFT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
