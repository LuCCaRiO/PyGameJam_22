import pygame as pg


class Group(pg.sprite.Group):
    def __init__(self):
        super(Group, self).__init__()

    def execute(self):
        for sprite in self.sprites():
            sprite.execute()
