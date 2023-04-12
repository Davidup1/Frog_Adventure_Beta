from random import randint
from pygame.sprite import Sprite


class Dice(Sprite):
    image_dict = {}
    level_list = ["BASIC", "SILVER", "GOLD"]

    def __init__(self, dice_type="ATTACK", level=0, special="", img_dict=None):
        super(Dice, self).__init__()
        if img_dict:
            Dice.image_dict = img_dict
        self.pointList = [1, 1, 1, 1, 1, 1]  # 点数列表
        self.point = 1
        self.type = dice_type  # "ATTACK" BLOCK BOOST HEAL MIRROR
        self.level = level
        self.special = special  # "CRYSTAL" HEAVY
        self.base_image = None
        self.image = None
        self.update_base_img()
        self.update_image()
        self.rect = self.image.get_rect()
        self.inBag = True
        self.generate_pointlist()

    def update_base_img(self):
        self.base_image = Dice.image_dict["type"][self.type].copy()
        self.base_image.blit(Dice.image_dict["level"][Dice.level_list[self.level]], (0, 0))
        if self.special:
            self.base_image.blit(Dice.image_dict["special"][self.special], (0, 0))

    def update_image(self):  # 仅更新点数
        self.image = self.base_image.copy()
        self.image.blit(Dice.image_dict["point"][str(self.point)], (0, 0))

    def upgrade(self):
        self.level += 1 if self.level <= 2 else 0
        self.generate_pointlist()
        self.update_base_img()

    def generate_pointlist(self):
        if self.type == "MIRROR":
            self.pointList = [4, 4, 4, 4, 4, 4]
        elif self.type == "BOOST":
            self.pointList[0] = self.level + 2
            self.pointList[1] = self.pointList[0]
            for i in range(2, 6):
                self.pointList[i] = randint(self.level if self.level else 1, self.level+2)
        else:
            self.pointList[0] = (self.level+1)*2
            self.pointList[1] = self.pointList[0]
            for i in range(2, 6):
                self.pointList[i] = randint(self.level*2 if self.level else 1, (self.level+1)*2)
        self.pointList.sort()

    def throw_dice(self):
        self.point = self.pointList[randint(0, 5)]

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