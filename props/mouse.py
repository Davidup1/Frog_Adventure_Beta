from pygame import Surface
from pygame.sprite import Sprite


class Mouse(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface((1, 1))
        self.rect = self.image.get_rect()
        self.button = False
        self.click = False
        self.cnt = 0
