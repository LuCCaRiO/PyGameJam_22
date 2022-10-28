import sys
import os
import pygame as pg
import time
import math
from settings import *
from menu import Menu
from player import Player
from entity import Entity
from tilemap import Tilemap
from camera import Camera
from item import Box
from text import Text
from ui import Ui
from jumpscare import Jumpscare
from sound import SoundController
from dark_view_field import DarkViewField


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(GAME_NAME)

        self.rendered_sprites = Camera()
        self.non_moving_sprites = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.exit_sprites = pg.sprite.Group()
        self.enemys = pg.sprite.Group()
        self.stations = pg.sprite.Group()
        self.controllers = pg.sprite.Group()

        self.place_sound = pg.mixer.Sound('./sfx/click.wav')

        self.players = [None, None]
        self.player_num = 0
        self.menu_entity = Menu(self.non_moving_sprites, (0, 0))

        self.item_list = []

        self.font = pg.font.SysFont('bahnschrift', 30)
        self.offset = pg.math.Vector2

        with open(f'{os.getcwd()}/savegame/level', 'r') as file:
            self.level = int(file.readline()[0])

        self.menu = True

    def run(self):
        clock = pg.time.Clock()
        while 1:
            delta_time = clock.tick(FPS)
            open_door = 0
            if not self.menu:
                for player in self.players:
                    if player.enemy_collision(delta_time):
                        self.reset()
                        self.create_world(self.level)
                if self.players[self.player_num].custom_collision(self.level, delta_time):
                    self.level += 1
                    with open(f'{os.getcwd()}/savegame/level', 'w') as file:
                        file.truncate()
                        file.writelines(str(self.level))
                    self.rendered_sprites.empty()
                    self.reset()
                    self.create_world(self.level)
                for sprite in self.stations.sprites():
                    if sprite.collision:
                        open_door += 1

            if self.menu:
                last_menu = self.menu
                self.menu = self.menu_entity.menu
                if last_menu != self.menu:
                    DarkViewField(self.non_moving_sprites, (0, 0))
                    Ui(self.non_moving_sprites, (0, SCREEN_HEIGHT - TILE_SIZE))
                    self.create_world(self.level)
                    SoundController(self.controllers)
            if self.players != [None, None]:
                self.item_list += self.players[self.player_num].return_list_of_items()
            self.rendered_sprites.update(delta_time, self.player_num, open_door, self.players)
            self.non_moving_sprites.update(self.item_list, delta_time, self.offset, self.players[self.player_num])
            self.controllers.update(delta_time)
            self.handle_events()
            self.render()

    def reset(self):
        self.rendered_sprites = Camera()
        self.items.empty()
        self.walls.empty()
        self.exit_sprites.empty()
        self.enemys.empty()
        self.stations.empty()
        self.players = [None, None]
        self.player_num = 0
        self.item_list = []
        pg.mixer.stop()

    def handle_events(self):
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    self.players[self.player_num].pressed_e()
                elif event.key == pg.K_SPACE and self.level > 2 and self.level != 5:
                    if self.player_num == 0:
                        self.player_num = 1
                    else:
                        self.player_num = 0
            elif event.type == pg.MOUSEBUTTONDOWN:
                for item in self.item_list:
                    if item == 'Box' and math.hypot(
                            int(self.players[self.player_num].rect.centerx / TILE_SIZE) * TILE_SIZE - int(
                                (mouse[0] + self.offset.x) / TILE_SIZE) * TILE_SIZE,
                            int(self.players[self.player_num].rect.centery / TILE_SIZE) * TILE_SIZE - int(
                                (mouse[1] + self.offset.y) / TILE_SIZE) * TILE_SIZE) <= TILE_SIZE * 1.5:
                        x = int((mouse[0] + self.offset.x) / TILE_SIZE) * TILE_SIZE
                        y = int((mouse[1] + self.offset.y) / TILE_SIZE) * TILE_SIZE
                        box = Box((self.rendered_sprites, self.items, self.walls), (x, y))
                        kill = False
                        merged_group = self.walls.sprites() + self.enemys.sprites() + self.players
                        for enemy in merged_group:
                            if box.rect.colliderect(enemy.rect) and enemy != box:
                                box.kill()
                                kill = True
                                break
                        if not kill:
                            self.item_list.remove(item)
                            self.place_sound.play()
                            break

    def tilemap(self, file):
        Tilemap(file, {WALL_KEY: (self.rendered_sprites, self.walls),
                       MONEMY_KEY: (self.rendered_sprites, self.enemys),
                       ITEM_KEY: (self.rendered_sprites, self.items, self.walls), NORMAL_KEY: self.rendered_sprites,
                       STATION_KEY: (self.rendered_sprites, self.stations),
                       DOOR_KEY: (self.rendered_sprites, self.walls),
                       EXIT_KEY: (self.rendered_sprites, self.exit_sprites), JUMPSCARE_KEY: self.non_moving_sprites,
                       TEXT_KEY: self.non_moving_sprites},
                {MONEMY_KEY: {WALL_KEY: self.walls, ITEM_KEY: self.items},
                 STATION_KEY: {ITEM_KEY: self.items}}).create_tilemap()

    def create_world(self, level):
        if level == 1:
            self.tilemap('./lvls/Level1.csv')
            self.players = []
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 5, TILE_SIZE * 5),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 0,
                                       self.non_moving_sprites))
            text = self.font.render('W, A, S, D TO MOVE', False, (255, 255, 255))
            Text(self.non_moving_sprites, text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 0))

        elif level == 2:
            self.tilemap('./lvls/Level2.csv')
            self.players = []
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 5, TILE_SIZE * 5),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 0,
                                       self.non_moving_sprites))
            text = self.font.render('E TO PICK UP BOXES', False, (255, 255, 255))
            text2 = self.font.render('LEFT MOUSE BUTTON TO PLACE DOWN BOXES', False, (255, 255, 255))
            Text(self.non_moving_sprites, text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 0))
            Text(self.non_moving_sprites, text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, text.get_height()))

        elif level == 3:
            self.tilemap('./lvls/Level3.csv')

            self.players = []
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 5, TILE_SIZE * 5),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 0,
                                       self.non_moving_sprites))
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 20, TILE_SIZE * 5),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 1,
                                       self.non_moving_sprites))
            text = self.font.render('SPACE TO SWITCH BETWEEN PLAYERS', False, (255, 255, 255))
            Text(self.non_moving_sprites, text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 0))
        elif level == 4:
            self.tilemap('./lvls/Level4.csv')
            self.players = []
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 3, TILE_SIZE * 2),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 0, self.non_moving_sprites))
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 20, TILE_SIZE * 6),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 1, self.non_moving_sprites))
        elif level == 5:
            self.tilemap('./lvls/Level5.csv')
            self.players = []
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 5, TILE_SIZE * 5),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 0, self.non_moving_sprites))
        elif level == 6:
            self.tilemap('./lvls/Level6.csv')
            self.players = []
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 4, TILE_SIZE),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 0, self.non_moving_sprites))
            self.players.append(Player(self.rendered_sprites, (TILE_SIZE * 15, TILE_SIZE * 5),
                                       {WALL_KEY: self.walls, ITEM_KEY: self.items, EXIT_KEY: self.exit_sprites,
                                        MONEMY_KEY: self.enemys}, 1, self.non_moving_sprites))

    def render(self):
        self.screen.fill((30, 26, 30))
        self.offset = self.rendered_sprites.custom_draw(self.screen, self.players[self.player_num],
                                                        f'./lvls/Level{self.level}.csv')
        self.non_moving_sprites.draw(self.screen)
        pg.display.update()


if __name__ == '__main__':
    pg.init()
    Game().run()
