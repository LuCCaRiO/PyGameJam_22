import pygame as pg
from entity import Entity
from settings import *


class Enemy(Entity):
    def __init__(self, groups, image, pos):
        super(Enemy, self).__init__(groups, image, pos)


MOVING_SPEED = 0.2
WAIT_SECONDS = 300


class Monemy(Enemy):  # Moveable Enemy
    def __init__(self, groups, pos):
        super(Monemy, self).__init__(groups, pg.transform.scale(pg.image.load('./imgs/Enemy.png'),
                                                                (TILE_SIZE * 3, TILE_SIZE * 3)), pos)
        self.speed = pg.math.Vector2(MOVING_SPEED, 0)
        self.time = 0

    def move(self, delta_time):
        self.rect.topleft += self.speed * delta_time

    def update(self, delta_time, player_num, open_door, players):
        self.speed.x += 0.0002
        self.time += delta_time
        if self.time > WAIT_SECONDS:
            self.move(delta_time)
