from pygame.sprite import Group
from pygame.sprite import Sprite

class Dice(Sprite):
    def __init__(self, style, img, level, is_heavy=False, is_crystal=False):
        self.pointList = [1, 1, 1, 1, 1, 1]  # 点数列表
        self.point = 1
        self.type = style  # "ATTACK" BLOCK BOOST HEAL MIRROR
        self.image = img.copy()
        self.hover_image = img.copy()
        self.init_image = img.copy()
        self.level = level  # "BASIC" SILVER GOLD
        self.heavy = is_heavy
        self.crystal = is_crystal
        self.mouseHover = False
        self.isDragged = False
        self.rect = self.image.get_rect()

    def onMouseHover(self, hover):
        if hover and not self.mouseHover:
            self.image = self.hover_image
        elif self.mouseHover and not hover:
            self.image = self.init_image
        self.mouseHover = hover

    def drag(self, dice, pos):
        if self.mouseHover and dice:
            self.isDragged = True
        elif not dice:
            self.isDragged = False
        if self.isDragged:
            self.rect.center = pos