import pygame as pg
import sys
from entity import Entity


LEFT_MOUSE = 0


class Button(Entity):
    def __init__(self, groups, image, pos):
        super(Button, self).__init__(groups, image, pos)
        self.clicked = False

    def get_clicked(self, func):
        left_mouse = pg.mouse.get_pressed()[LEFT_MOUSE]
        if left_mouse and not self.clicked:
            self.clicked = True
            func()
        elif not left_mouse and self.clicked:
            self.clicked = False


class MenuButton(Button):
    def __init__(self, groups, image, pos):
        super(MenuButton, self).__init__(groups, image, pos)
        self.menu = True

    def execute(self):
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.menu = False

    def update(self):
        self.get_clicked(self.execute)


class QuitButton(Button):
    def __init__(self, groups, image, pos):
        super(QuitButton, self).__init__(groups, image, pos)

    def execute(self):
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            sys.exit()

    def update(self):
        self.get_clicked(self.execute)
