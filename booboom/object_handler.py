import typing
from random import choices, randrange

from booboom.npc import NPC
from booboom.sprite_object import AnimatedSprite

if typing.TYPE_CHECKING:
    from booboom.main import Game


class ObjectHandler:
    def __init__(self, game: "Game"):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_positions = {}
        # spawn npc
        self.enemies = 5
        self.npc_types = [NPC]
        self.weights = [100]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_npc()

        # Sprites
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_yellow", (10.5, 3.5), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_yellow", (1.5, 1.5), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_yellow", (1.5, 7.5), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_yellow", (5.5, 3.25), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_yellow", (5.5, 4.75), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_yellow", (7.5, 2.5), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_yellow", (7.5, 5.5), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_yellow", (14.5, 1.5), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_red", (14.5, 7.5), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_red", (12.5, 7.5), 0.7, 0.27, 120))
        self.add_sprite(AnimatedSprite(self.game, "torch_animated_red", (9.5, 7.5), 0.7, 0.27, 120))

        self.portal = None
        self.portal_tile = None
        self.last_died_npc = None

    def get_random_allowed_pos(self):
        pos = randrange(self.game.map.cols), randrange(self.game.map.rows)
        while (pos in self.game.map.world_map) or (pos in self.restricted_area) or (pos in self.npc_positions):
            pos = randrange(self.game.map.cols), randrange(self.game.map.rows)
        return pos

    def spawn_npc(self):
        for i in range(self.enemies):
            npc = choices(self.npc_types, self.weights)[0]
            x, y = self.get_random_allowed_pos()
            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def spawn_portal(self):
        x, y = self.last_died_npc.x, self.last_died_npc.y
        self.portal_tile = (int(x), int(y))
        self.portal = AnimatedSprite(self.game, "win_portal", (x, y))

    def check_portal_spawn(self):
        if self.portal is None and len(self.npc_positions) == 0:
            self.spawn_portal()

    def update_npc_positions(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}

    def update(self):
        self.update_npc_positions()
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()
        if self.portal is not None:
            self.portal.update()
        self.check_portal_spawn()

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_npc(self, npc):
        self.npc_list.append(npc)
        self.update_npc_positions()
