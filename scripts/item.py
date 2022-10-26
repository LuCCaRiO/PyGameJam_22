import pygame as pg
from entity import Entity
from settings import *


class Item(Entity):
    def __init__(self, groups, image, pos):
        super(Item, self).__init__(groups, pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)), pos)


class Box(Item):
    def __init__(self, groups, pos):
        super(Box, self).__init__(groups, pg.image.load('./imgs/tiles/Box.png'), pos)
