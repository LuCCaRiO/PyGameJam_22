import pygame as pg
import math
from entity import Entity
from jumpscare import Jumpscare
from settings import *


class Tile(Entity):
    def __init__(self, groups, image, pos):
        super(Tile, self).__init__(groups, pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)), pos)


class StationTile(Tile):
    def __init__(self, groups, image, pos, collidable_groups):
        super(StationTile, self).__init__(groups, image, pos)
        self.collidable_groups = collidable_groups
        self.collision = False

    def custom_collision(self):
        self.collision = False
        for sprite in self.collidable_groups[ITEM_KEY]:
            if sprite.rect.colliderect(self.rect):
                self.collision = True

    def update(self, delta_time, player_num, open_door, players):
        self.custom_collision()


class DoorTile(Tile):
    def __init__(self, groups, pos, keys):
        super(DoorTile, self).__init__(groups, pg.image.load('./imgs/tiles/Door.png'), pos)
        self.groups_ = groups
        self.keys = keys

    def update(self, delta_time, player_num, open_door, players):
        if open_door >= self.keys:
            self.kill()


DISTANCE = 100


class FakeBox(Tile):
    def __init__(self, groups, pos, jumpscare_groups):
        super(FakeBox, self).__init__(groups, pg.image.load('./imgs/tiles/Box.png'), pos)
        self.jumpscare_groups = jumpscare_groups

    def update(self, delta_time, player_num, open_door, players):
        distance = math.hypot(self.rect.centerx - players[player_num].rect.centerx,
                              self.rect.centery - players[player_num].rect.centery)
        if distance <= DISTANCE:
            Jumpscare(self.jumpscare_groups, (0, 0))
            self.kill()
