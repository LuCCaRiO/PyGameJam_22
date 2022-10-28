import pygame as pg
import os
import csv
from tile import Tile, StationTile, DoorTile, FakeBox, FakeTile
from enemy import Monemy
from item import Box
from settings import *


class Tilemap:
    def __init__(self, file_name, groups, collidable_groups):
        self.file_name = file_name
        self.groups = groups
        self.collidable_groups = collidable_groups

    @staticmethod
    def read_csv(file_name):
        map_ = []
        with open(os.path.join(file_name)) as data:
            data = csv.reader(data, delimiter=',')
            for column in data:
                map_.append(list(column))
        return map_

    def create_tilemap(self):
        map_ = self.read_csv(self.file_name)
        for i in range(len(map_)):
            for j, row in enumerate(map_[i]):
                if '1' in row and row != '-1':
                    Tile(self.groups[WALL_KEY], pg.image.load('./imgs/tiles/tile_2.png'),
                         (TILE_SIZE * j, TILE_SIZE * i))
                if '0' in row:
                    Box(self.groups[ITEM_KEY], (TILE_SIZE * j, TILE_SIZE * i))
                if '2' in row:
                    Tile(self.groups[NORMAL_KEY], pg.image.load('./imgs/tiles/New Piskel.png'),
                         (TILE_SIZE * j, TILE_SIZE * i))
                if '3' in row:
                    DoorTile(self.groups[DOOR_KEY], (TILE_SIZE * j, TILE_SIZE * i), 1)
                if '7' in row:
                    DoorTile(self.groups[DOOR_KEY], (TILE_SIZE * j, TILE_SIZE * i), 2)
                if '4' in row:
                    StationTile(self.groups[STATION_KEY], pg.image.load('./imgs/tiles/box_place.png'),
                                (TILE_SIZE * j, TILE_SIZE * i), self.collidable_groups[STATION_KEY])
                if '5' in row:
                    Tile(self.groups[EXIT_KEY], pg.image.load('./imgs/tiles/exit_tile.png'),
                         (TILE_SIZE * j, TILE_SIZE * i))
                if '6' in row:
                    FakeTile(self.groups[WALL_KEY], (TILE_SIZE * j, TILE_SIZE * i), self.groups[MONEMY_KEY], (TILE_SIZE, TILE_SIZE), self.groups[TEXT_KEY])
                if '8' in row:
                    FakeBox(self.groups[NORMAL_KEY], (TILE_SIZE * j, TILE_SIZE * i), self.groups[JUMPSCARE_KEY])
