import time
from entity import Entity

END_TIME = 5000


class Text(Entity):
    def __init__(self, groups, image, pos):
        super(Text, self).__init__(groups, image, pos)
        self.time = 0
        self.ghost = 255

    def execute(self, bool_):
        if bool_:
            self.kill()

    def update(self, item_list, delta_time, offset, player):
        self.time += delta_time
        if self.time >= END_TIME:
            image = self.image.copy()
            self.ghost -= delta_time / 5
            if self.ghost <= 0:
                self.kill()
            image.set_alpha(self.ghost)
            self.image = image
