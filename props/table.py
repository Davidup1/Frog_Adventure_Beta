from pygame.sprite import Sprite
from pygame.sprite import Group
from buildingTool.animation import Animation
import pygame
import json

FLOAT_DURATION = 180


class Cell(Sprite):
    def __init__(self, index, pos, point_card=None):
        super().__init__()
        self.index = index
        self.image = pygame.Surface((48, 48))
        self.image.set_alpha(60)
        self.rect = self.image.get_rect()
        self.selected_image = self.image.copy()
        self.enhanced_image = self.image.copy()
        self.image.set_alpha(0)
        self.init_image = self.image.copy()
        self.pointCard = point_card.copy() if point_card else None
        pygame.draw.rect(self.selected_image, (100, 255, 255), self.rect)
        pygame.draw.rect(self.enhanced_image, (255, 255, 100), self.rect)
        self.rect.center = pos
        self.init_rect = self.rect.copy()


class TableMain(Sprite):
    def __init__(self, img, point_card):
        super().__init__()
        self.init_image = img.copy()
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (292, 60)  # 38*38
        self.init_rect = self.rect.copy()
        self.dice_list = [None]*9
        self.dice_remain = 0
        self.cellList = []
        self.posList = [
                        (481, 157),
                    (424, 214), (538, 214),
            (367, 271), (481, 271), (595, 271),
                    (424, 328), (538, 328),
                        (481, 385)
        ]
        for index, pos in enumerate(self.posList):
            self.cellList.append(Cell(index, (pos[0], pos[1]-19), point_card))
        self.cellMap = [
            [0, 1, 1, 2, 2, 2, 3, 3, 4],
            [1, 0, 2, 1, 1, 3, 2, 2, 3],
            [1, 2, 0, 3, 1, 1, 2, 2, 3],
            [2, 1, 3, 0, 2, 4, 1, 3, 2],
            [2, 1, 1, 2, 0, 2, 1, 1, 2],
            [2, 3, 1, 4, 2, 0, 3, 1, 2],
            [3, 2, 2, 1, 1, 3, 0, 2, 1],
            [3, 2, 2, 3, 1, 1, 2, 0, 1],
            [4, 3, 3, 2, 2, 2, 1, 1, 0]
        ]
        self.animation = Animation()
        self.animation.float(FLOAT_DURATION, 3)
        self.calculate_list = []
        for i in range(9):
            self.calculate_list.append(["", 0])
        self.sum = {"ATTACK": 0, "BLOCK": 0, "HEAL": 0}

    def update_image(self):
        pos = self.animation.play(self.init_rect)
        if pos:
            self.rect.topleft = pos
        self.dice_remain = 0
        for index in range(9):
            dice = self.dice_list[index]
            if dice and not dice.isDragged:
                self.dice_remain += 1
                dice.rect.center = self.cellList[index].rect.center

    def onMouseHover(self, cells, mouse):
        mouse.cur_cell = None
        for cell in self.cellList:
            cell.image = cell.init_image
            pos = cell.init_rect.topleft
            cell.rect.topleft = pos[0], pos[1]+self.animation.animationList[self.animation.curFrame]
        dice = mouse.cur_dice
        if dice:
            for cell in cells:
                if cell in self.cellList:
                    # mouse.cur_cell = cell
                    # if mouse.cur_cell:
                    #     print(mouse.cur_cell)
                    cell.image = cell.selected_image
                    mouse.cur_cell = cell
                    if dice.type == "BOOST":
                        for index, distance in enumerate(self.cellMap[cell.index]):
                            if distance == dice.point:
                                self.cellList[index].image = self.cellList[index].enhanced_image
            if mouse.button_up and mouse.cur_cell:
                index = self.cellList.index(mouse.cur_cell)
                if not self.dice_list[index]:
                    if dice in self.dice_list:
                        self.dice_list[self.dice_list.index(dice)] = None
                    self.dice_list[index] = dice
                    dice.set_pos(self.posList[index], "center")
                    dice.shift_place("table")

    def take_out_dice(self, dice,num=0):
        if num:
            print(self.dice_list)
            print(self.dice_list.index(dice))
        self.dice_list[self.dice_list.index(dice)] = None

    def calculate(self, game):
        self.sum = {"ATTACK": 0, "BLOCK": 0, "HEAL": 0}
        self.calculate_list = []
        for i in range(9):
            self.calculate_list.append(["", 0])
        for index in range(9):
            dice = self.dice_list[index]
            if dice:
                if dice.type in ["ATTACK", "BLOCK", "HEAL"]:
                    self.calculate_list[index][0] = dice.type
                    self.calculate_list[index][1] += dice.point
                elif dice.type == "BOOST":
                    for i, distance in enumerate(self.cellMap[index]):
                        if distance == dice.point:
                            self.calculate_list[i][1] += dice.point
                elif dice.type == "MIRROR":
                    for i, distance in enumerate(self.cellMap[index]):
                        if distance == 4:
                            self.calculate_list[i][1] *= 2
        for index in range(9):
            data = self.calculate_list[index]
            self.cellList[index].pointCard.update_image(data[1])
            if data[0]:
                self.sum[data[0]] += data[1]
        # print(self.dice_list, '\n', self.calculate_list, "\n", self.sum)
        game.player.balls['DEF'].num = self.sum["BLOCK"]
        game.player.balls['Heal'].num = self.sum["HEAL"]
        game.monsters[-1].balls['ATK'].num = self.sum["ATTACK"]


class TableBtn(Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img.copy()
        self.init_image = img.copy()
        self.rect = self.image.get_rect()
        self.hover_image = img.copy()
        pygame.draw.rect(img, (255, 255, 255, 40), self.rect)
        self.hover_image.blit(img, (0, 0))
        self.rect.topleft = (320, 60)
        self.init_rect = self.rect.copy()
        self.mouseHover = False
        self.isDragged = False
        self.animation = Animation()
        self.animation.float(FLOAT_DURATION, 5)

    def update_image(self):
        pos = self.animation.play(self.init_rect)
        if pos:
            self.rect.topleft = pos

    def onMouseHover(self, hover):
        if hover and not self.mouseHover:  # 鼠标在btn上
            self.image = self.hover_image
        elif self.mouseHover and not hover:
            self.image = self.init_image
        self.mouseHover = hover

    def onClick(self, click, game):
        if self.mouseHover and click:
            game.roundFinish = True
            game.tableGroup.tableMain.animation.quadratic(50, (1, 16), 7)
            self.animation.quadratic(50, (1, 16), 7)
            game.delay = 60
            game.flag = ["player","attack"]
            for dice in game.bag1.all_dices:
                if dice.where != "bag":
                    dice.able = False
                    dice.update_image()
                # print(dice.type, dice.where, dice.able)
        if game.status == "online":
            self.sendSum(game,game.tableGroup.tableMain.sum)


    def sendSum(self,game, sum):
        message = json.dumps(sum)
        game.broadcast.sendto(message.encode('utf-8'), (game.targetIP, 10131))

class Table(Group):
    def __init__(self, img, point_card):
        super().__init__()
        self.tableMain = TableMain(img[0], point_card)
        self.tableBtn = TableBtn(img[1])
        self.add(self.tableMain)
        self.add(self.tableBtn)
        for cell in self.tableMain.cellList:
            self.add(cell)

    def collisionDetection(self, game):
        mouse = game.mouse
        result = pygame.sprite.spritecollide(mouse, self, False)
        self.tableBtn.onMouseHover(self.tableBtn in result)
        self.tableBtn.onClick(mouse.button_up, game)
        self.tableMain.onMouseHover(result, mouse)

    def eventHandle(self, game):
        self.collisionDetection(game)
        self.tableBtn.update_image()
        self.tableMain.update_image()

    def back(self):
        self.tableBtn.animation.backward()
        self.tableMain.animation.backward()


