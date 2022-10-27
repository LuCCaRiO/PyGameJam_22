import pygame as pg
from entity import Entity
from settings import *


class Enemy(Entity):
    def __init__(self, groups, image, pos):
        super(Enemy, self).__init__(groups, image, pos)


MOVING_SPEED = 0.15


class Monemy(Enemy):  # Moveable Enemy
    def __init__(self, groups, pos, collidable_groups):
        super(Monemy, self).__init__(groups, pg.transform.scale(pg.image.load('./imgs/Enemy.png'),
                                                                (TILE_SIZE * 3, TILE_SIZE * 3)), pos)
        self.speed = pg.math.Vector2(MOVING_SPEED, 0)
        self.collidable_groups = collidable_groups

    def set_speed(self):
        merged_groups = self.collidable_groups[WALL_KEY].sprites() + self.collidable_groups[ITEM_KEY].sprites()
        for sprite in merged_groups:
            if self.rect.colliderect(sprite.rect):
                if self.speed.x > 0:
                    self.rect.right = sprite.rect.left
                elif self.speed.x < 0:
                    self.rect.left = sprite.rect.right
                self.speed.x *= -1

    def move(self, delta_time):
        self.rect.topleft += self.speed * delta_time

    def update(self, delta_time, player_num, open_door, players):
        self.set_speed()
        self.move(delta_time)
