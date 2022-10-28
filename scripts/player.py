import math
import sys
import os
from text import Text
import pygame as pg
from settings import *
from entity import Entity
from item import Box
from jumpscare import Jumpscare

MOVING_SPEED = 0.2
ANIMATION_SPEED = 0.01

P_WIDTH = TILE_SIZE * 0.4
P_HEIGHT = TILE_SIZE * 0.6

MAX_TIME = 2000


class Player(Entity):
    def __init__(self, groups, pos, collidable_groups, id_, jumpscare_groups):
        self.sheet = (
            pg.transform.scale(pg.image.load('./imgs/player_sheet/Layer 1_player_sheet1.png'), (P_WIDTH, P_HEIGHT)),
            pg.transform.scale(pg.image.load('./imgs/player_sheet/Layer 1_player_sheet2.png'), (P_WIDTH, P_HEIGHT)),
            pg.transform.scale(pg.image.load('./imgs/player_sheet/Layer 1_player_sheet3.png'), (P_WIDTH, P_HEIGHT)),
            pg.transform.scale(pg.image.load('./imgs/player_sheet/Layer 1_player_sheet4.png'), (P_WIDTH, P_HEIGHT)))
        self.image_index = 0
        super(Player, self).__init__(groups, self.sheet[self.image_index], pos)
        self.speed = pg.math.Vector2()
        self.state = IDLE
        self.flip = False
        self.pick_up = False
        self.time = 0
        self.jumpscare = False
        self.pick_up_sound = pg.mixer.Sound('./sfx/click.wav')
        self.collidable_groups = collidable_groups
        self.id = id_
        self.font = pg.font.SysFont('bahnschrift', 100)
        self.jumpscare_groups = jumpscare_groups
        self.exit = False

    def input(self):
        self.speed = pg.math.Vector2()
        self.state = IDLE
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            self.speed.y = -MOVING_SPEED
            self.state = WALK_UP
        elif key[pg.K_s]:
            self.speed.y = MOVING_SPEED
            self.state = WALK_DOWN

        if key[pg.K_a]:
            self.speed.x = -MOVING_SPEED
            self.state += WALK_LEFT
            self.flip = True
        elif key[pg.K_d]:
            self.speed.x = MOVING_SPEED
            self.state += WALK_RIGHT
            self.flip = False

    def pressed_e(self):
        self.pick_up = True

    def vertical_collision(self):
        for sprite in self.collidable_groups[WALL_KEY]:
            if sprite.rect.colliderect(self.rect):
                self.speed.y = 0
                if WALK_DOWN in self.state:
                    self.rect.bottom = sprite.rect.top
                else:
                    self.rect.top = sprite.rect.bottom

    def horizontal_collision(self):
        for sprite in self.collidable_groups[WALL_KEY]:
            if sprite.rect.colliderect(self.rect):
                self.speed.x = 0
                if WALK_RIGHT in self.state:
                    self.rect.right = sprite.rect.left
                else:
                    self.rect.left = sprite.rect.right

    def return_list_of_items(self):
        list_of_items = []
        for sprite in self.collidable_groups[ITEM_KEY]:
            if self.pick_up and math.hypot(self.rect.centerx - sprite.rect.centerx,
                                           self.rect.centery - sprite.rect.centery) <= TILE_SIZE * 1.5:
                list_of_items.append(sprite.__class__.__name__)
                self.pick_up_sound.play()
                sprite.kill()
        return list_of_items

    def custom_collision(self, level, delta_time):
        if self.exit and self.time < MAX_TIME:
            self.time += delta_time
        elif self.exit and self.time > MAX_TIME:
            with open(f'{os.getcwd()}\savegame\level', 'w') as file:
                file.truncate()
                file.writelines('1')
            sys.exit()

        for sprite in self.collidable_groups[EXIT_KEY]:
            if self.rect.colliderect(sprite.rect):
                if level >= 6:
                    image = pg.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    image.fill((0, 0, 0))
                    text = self.font.render('YOU ESCAPED', False, (255, 0, 0))
                    image.blit(text,
                               (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
                    Text(self.jumpscare_groups, image, (0, 0))
                    sprite.kill()
                    self.time = 0
                    self.exit = True
                else:
                    return True
        return False

    def animation(self, delta_time):
        if self.state != IDLE:
            self.image_index += ANIMATION_SPEED * delta_time
            if int(self.image_index) >= len(self.sheet) - 1:
                self.image_index = 0
            self.image = pg.transform.flip(self.sheet[int(self.image_index)], self.flip, False)
        elif self.sheet != 0:
            self.image = pg.transform.flip(self.sheet[0], self.flip, False)

    def move(self, delta_time):
        self.rect.x += self.speed.x * delta_time
        self.horizontal_collision()
        self.rect.y += self.speed.y * delta_time
        self.vertical_collision()

    def enemy_collision(self, delta_time):
        if self.jumpscare and self.time < MAX_TIME:
            self.time += delta_time
        for sprite in self.collidable_groups[MONEMY_KEY]:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                Jumpscare(self.jumpscare_groups, (0, 0))
                self.jumpscare = True
        if self.time > MAX_TIME and self.jumpscare:
            self.jumpscare = False
            return True
        else:
            return False

    def update(self, delta_time, player_num, open_door, players):
        self.pick_up = False
        if self.id == player_num:
            self.input()
            self.move(delta_time)
        self.animation(delta_time)
