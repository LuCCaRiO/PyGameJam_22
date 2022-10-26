import pygame as pg
from entity import Entity
from button import MenuButton, QuitButton
from group import Group
from settings import *


class Menu(Entity):
    def __init__(self, groups, pos):
        image = pg.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        image.blit(pg.transform.scale(pg.image.load('./imgs/Menu.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        self.rendered_sprites = pg.sprite.Group()
        self.menu_buttons = pg.sprite.Group()
        MenuButton((self.rendered_sprites, self.menu_buttons),
                   pg.transform.scale(pg.image.load('./imgs/start_button.png'), (256, 100)),
                   (SCREEN_WIDTH / 2 - 128, SCREEN_HEIGHT / 2 - 50))
        QuitButton(self.rendered_sprites,
                   pg.transform.scale(pg.image.load('./imgs/quit_button.png'), (256, 100)),
                   (SCREEN_WIDTH / 2 - 128, SCREEN_HEIGHT / 2 + 100))
        super(Menu, self).__init__(groups, image, pos)
        self.menu = True

    def update(self, item_list, delta_time, offset, player):
        self.set_menu()
        self.rendered_sprites.update()
        self.rendered_sprites.draw(self.image)

    def set_menu(self):
        for sprite in self.menu_buttons.sprites():
            if not sprite.menu:
                self.menu = False
                self.kill()
                break
