import pygame as pg
import math
from entity import Entity
from settings import *


class Ui(Entity):
    def __init__(self, groups, pos):
        image = pg.surface.Surface((SCREEN_WIDTH, TILE_SIZE))
        super(Ui, self).__init__(groups, image, pos)
        self.font = pg.font.SysFont('bahnschrift', 30)

    def render(self, item_list):
        self.image.blit(pg.transform.scale(pg.image.load('./imgs/Ui.png'), (SCREEN_WIDTH, TILE_SIZE)), (0, 0))
        text = self.font.render('ITEMS', False, (0, 0, 0))
        self.image.blit(text, ((len(item_list) * TILE_SIZE) + SCREEN_WIDTH // 64, 0))
        for item in range(len(item_list)):
            self.image.blit(
                pg.transform.scale(pg.image.load(f'./imgs/tiles/{item_list[item]}.png'), (TILE_SIZE, TILE_SIZE)),
                (item * TILE_SIZE, 0))

    def update(self, item_list, delta_time, offset, player):
        self.render(item_list)
