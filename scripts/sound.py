import pygame as pg
import random


class SoundController(pg.sprite.Sprite):
    def __init__(self, groups):
        super(SoundController, self).__init__(groups)
        pg.mixer.Sound('./sfx/zoomc.wav').play()
        self.time = 0
        self.wait_time = random.randint(60, 60)
        self.knock_sound = pg.mixer.Sound('./sfx/knock.mp3')

    def update(self, delta_time):
        self.time += delta_time
        if self.time > self.wait_time * 1000:
            self.time = 0
            self.wait_time = random.randint(60, 60)
            self.knock_sound.play()

