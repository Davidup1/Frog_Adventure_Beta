from pygame import Rect
from pygame.sprite import Sprite


class Mouse(Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect((0, 0, 1, 1))
        self.button = False
        self.cnt = 0
