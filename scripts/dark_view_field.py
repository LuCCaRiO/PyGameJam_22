import pygame as pg
from entity import Entity
from settings import *


class DarkViewField(Entity):
    def __init__(self, groups, pos):
        super(DarkViewField, self).__init__(groups, pg.transform.scale(pg.image.load('./imgs/vignette.png'),
                                                                       (SCREEN_WIDTH * 5, SCREEN_HEIGHT * 5)), pos)

    def update(self, item_list, delta_time, offset, player):
        self.rect.topleft += player.rect.center - offset - self.rect.topleft - (self.rect.w // 2, self.rect.h // 2)
