import math
import random
import pygame as pg
from entity import Entity
from settings import *


class DarkViewField(Entity):
    def __init__(self, groups, pos):
        width = SCREEN_WIDTH * 5
        height = SCREEN_HEIGHT * 5
        super(DarkViewField, self).__init__(groups, pg.transform.scale(pg.image.load('./imgs/vignette.png'), (width, height)), pos)
        self.time = 0
        self.stop_time = random.randint(1, 5)

    def update(self, item_list, delta_time, offset, player):
        self.time += delta_time
        self.rect.topleft += player.rect.center - offset - self.rect.topleft - (self.rect.w // 2, self.rect.h // 2)
