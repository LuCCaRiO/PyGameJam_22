import pygame as pg
from settings import *
from item import Box
from tilemap import Tilemap
import random

SMOOTHNESS = 7


class Camera(pg.sprite.Group):
    def __init__(self):
        super(Camera, self).__init__()
        self.offset = pg.math.Vector2()

    def custom_draw(self, screen, player, file):
        if player is not None:
            width = len(Tilemap.read_csv(file)[0])
            height = len(Tilemap.read_csv(file)) + 1
            if SCREEN_WIDTH // 2 <= player.rect.centerx <= (width * TILE_SIZE) - SCREEN_WIDTH // 2:
                self.offset.x += ((player.rect.centerx - SCREEN_WIDTH // 2) - self.offset.x) / SMOOTHNESS

            elif player.rect.centerx <= (
                    width * TILE_SIZE) - SCREEN_WIDTH // 2 and player.rect.centerx <= SCREEN_WIDTH // 2:
                self.offset.x += self.offset.x / -SMOOTHNESS

            elif player.rect.centerx >= width * TILE_SIZE - SCREEN_WIDTH // 2:
                self.offset.x += ((width * TILE_SIZE - SCREEN_WIDTH) - self.offset.x) / SMOOTHNESS

            if SCREEN_HEIGHT // 2 <= player.rect.centery <= (height * TILE_SIZE) - SCREEN_HEIGHT // 2:
                self.offset.y += ((player.rect.centery - SCREEN_HEIGHT // 2) - self.offset.y) / SMOOTHNESS

            elif player.rect.centery <= (
                    height * TILE_SIZE) - SCREEN_HEIGHT // 2 and not player.rect.centery >= SCREEN_HEIGHT // 2:
                self.offset.y += self.offset.y / -SMOOTHNESS
            elif player.rect.centery >= height * TILE_SIZE - SCREEN_HEIGHT // 2:

                self.offset.y += ((height * TILE_SIZE - SCREEN_HEIGHT) - self.offset.y) / SMOOTHNESS

        for sprite in sorted(self.sprites(), key=lambda sprite_: isinstance(sprite_, Box)):
            screen.blit(sprite.image, sprite.rect.topleft - self.offset)
        return self.offset
