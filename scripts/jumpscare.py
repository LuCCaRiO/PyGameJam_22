import pygame as pg
import random
import math
from entity import Entity
from settings import *

MAX_TIME = 2000


class Jumpscare(Entity):
    def __init__(self, groups, pos):
        super(Jumpscare, self).__init__(groups, pg.transform.scale(pg.image.load('./imgs/Jumpscare.png'),
                                                                   (SCREEN_WIDTH, SCREEN_HEIGHT)), pos)
        pg.mixer.Sound('./sfx/Jumpscare.wav').play()
        self.time = 0

    def update(self, item_list, delta_time, offset, player):
        self.rect.topleft = pg.math.Vector2(random.randint(-5, 5), random.randint(-5, 5))
        self.time += delta_time
        if self.time >= MAX_TIME:
            self.kill()