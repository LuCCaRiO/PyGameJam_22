import pygame as pg


class Entity(pg.sprite.Sprite):
    def __init__(self, groups, image, pos):
        super(Entity, self).__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
