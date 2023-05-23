from random import randint
from pygame.sprite import Sprite
import pygame


class Dice(Sprite):
    image_dict = {}
    level_list = ["BASIC", "SILVER", "GOLD"]
    able_place = ["table", "diceTable"]
    unable_place = ["bag"]
    places = {"bag":None, "diceTable":None, "table":None}
    CNT = 0

    def __init__(self, dice_type="ATTACK", level=0, special="", img_dict=None):
        super(Dice, self).__init__()
        Dice.CNT += 1
        self.num = Dice.CNT
        if img_dict:
            Dice.image_dict = img_dict
            Dice.image_dict["type"]["mask"].set_alpha(150)
        self.able = True
        self.pointList = [1, 1, 1, 1, 1, 1]  # 点数列表
        self.pointIndex = 0
        self.point = 1
        self.type = dice_type  # "ATTACK" BLOCK BOOST HEAL MIRROR
        self.level = level
        self.special = special  # "CRYSTAL" HEAVY
        self.base_image = None
        self.image = None
        self.update_base_img()
        self.update_image()
        self.rect = self.image.get_rect()
        self.where = "bag"  # diceTable table mouse
        self.generate_pointlist()
        self.init_pos = (0, 0)
        self.isDragged = False
        self.mouseHover = False

    def bind(self, bag, table, diceTable):
        Dice.places["bag"] = bag
        Dice.places["table"] = table
        Dice.places["diceTable"] = diceTable

    def copy(self):
        dice = Dice(self.type, self.level, self.special)
        dice.pointList = self.pointList
        dice.base_image = self.base_image
        dice.image = self.image
        dice.rect = self.rect
        dice.where = self.where
        return dice

    def set_pos(self, pos, mode=None):
        if mode == "center":
            self.rect.center = pos
            self.init_pos = self.rect.topleft
        else:
            self.init_pos = self.rect.topleft = pos

    def update_base_img(self):
        self.base_image = Dice.image_dict["type"][self.type].copy()
        self.base_image.blit(Dice.image_dict["level"][Dice.level_list[self.level]], (0, 0))
        if self.special:
            self.base_image.blit(Dice.image_dict["special"][self.special], (0, 0))

    def update_image(self):  # 仅更新点数
        self.image = self.base_image.copy()
        self.point = self.pointList[self.pointIndex]
        self.image.blit(Dice.image_dict["point"][str(self.point)], (0, 0))
        if not self.able:
            self.image.blit(Dice.image_dict["type"]["mask"], (0, 0))

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
        self.pointIndex = randint(0, 5)
        self.point = self.pointList[self.pointIndex]
        self.update_image()

    def onMouseHover(self, mouse):
        hover = pygame.sprite.collide_rect(mouse, self)
        if hover:
            mouse.cur_dice = self
            if not self.mouseHover:  # 移入
                pass
        else:
            if mouse.cur_dice == self:
                mouse.cur_dice = None
            elif self.mouseHover:  # 移出
                pass
        self.mouseHover = hover

    def drag(self, mouse):
        if self.able:
            if self.mouseHover and mouse.button_down and self.where in Dice.able_place:
                self.isDragged = True
                self.init_pos = self.rect.topleft

            if self.isDragged:
                self.rect.center = mouse.rect.topleft
                if mouse.button_up:
                    self.isDragged = False
                    self.rect.topleft = self.init_pos

    def shift_place(self, to_where):
        if to_where != self.where:
            Dice.places[self.where].take_out_dice(self)
            self.where = to_where

    def eventHandle(self, mouse):
        self.onMouseHover(mouse)
        self.drag(mouse)
