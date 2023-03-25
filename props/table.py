from pygame.sprite import Sprite
from pygame.sprite import Group
import pygame


class TableMain(Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (289, 79)  # 38*38


class TableBtn(Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = self.init_image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (322, 78)
        self.mouseHover = False

    def onMouseHover(self, hover):
        if hover and not self.mouseHover:  # 鼠标在btn上
            print("放在btn上方")
            self.mouseHover = hover
        elif self.mouseHover and not hover:
            print("鼠标移开了")
            self.mouseHover = hover


class Table(Group):
    def __init__(self, img=[]):
        super().__init__()
        self.tableMain = TableMain(img[0])
        self.tableBtn = TableBtn(img[1])
        self.add(self.tableMain)
        self.add(self.tableBtn)

    def collisionDetection(self, mouse):
        self.tableBtn.onMouseHover(self.tableBtn in pygame.sprite.spritecollide(mouse, self, False))
