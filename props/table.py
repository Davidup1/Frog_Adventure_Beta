from pygame.sprite import Sprite
from pygame.sprite import Group
import pygame


class Cell(Sprite):
    def __init__(self, index, pos):
        super().__init__()
        self.index = index
        self.image = pygame.Surface((37, 37))
        self.image.set_alpha(60)
        self.rect = self.image.get_rect()
        self.selected_image = self.image.copy()
        self.enhanced_image = self.image.copy()
        self.image.set_alpha(0)
        self.init_image = self.image.copy()
        pygame.draw.rect(self.selected_image, (100, 255, 255), self.rect)
        pygame.draw.rect(self.enhanced_image, (255, 255, 100), self.rect)
        self.rect.topleft = pos


class TableMain(Sprite):
    def __init__(self, img):
        super().__init__()
        self.init_image = img.copy()
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (289, 79)  # 38*38
        self.cellList = []
        for index, pos in enumerate([
                        (460, 139),
                    (403, 196), (517, 196),
            (346, 253), (460, 253), (574, 253),
                    (403, 310), (517, 310),
                        (460, 367)
        ]):
            self.cellList.append(Cell(index, pos))
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

    def onMouseHover(self, cells, cnt):  # cnt之后换为dice.point  (if dice.type == "enhance")
        for cell in self.cellList:
            cell.image = cell.init_image
        for cell in cells:
            if cell in self.cellList:
                cell.image = cell.selected_image
                for index, distance in enumerate(self.cellMap[cell.index]):
                    if distance == cnt%5:
                        self.cellList[index].image = self.cellList[index].enhanced_image



class TableBtn(Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img.copy()
        self.init_image = img.copy()
        self.rect = self.image.get_rect()
        self.hover_image = img.copy()
        pygame.draw.rect(img, (255, 255, 255, 40), self.rect)
        self.hover_image.blit(img, (0, 0))
        self.rect.topleft = (322, 78)
        self.mouseHover = False
        self.isDragged = False

    def onMouseHover(self, hover):
        if hover and not self.mouseHover:  # 鼠标在btn上
            self.image = self.hover_image
        elif self.mouseHover and not hover:
            self.image = self.init_image
        self.mouseHover = hover

    def drag(self, button, pos):
        if self.mouseHover and button:
            self.isDragged = True
        elif not button:
            self.isDragged = False
        if self.isDragged:
            self.rect.center = pos


class Table(Group):
    def __init__(self, img=[]):
        super().__init__()
        self.tableMain = TableMain(img[0])
        self.tableBtn = TableBtn(img[1])
        self.add(self.tableMain)
        self.add(self.tableBtn)
        for cell in self.tableMain.cellList:
            self.add(cell)

    def collisionDetection(self, mouse, cnt):
        result = pygame.sprite.spritecollide(mouse, self, False)
        self.tableBtn.onMouseHover(self.tableBtn in result)
        self.tableMain.onMouseHover(result, cnt)

    def eventHandle(self, game):
        self.collisionDetection(game.mouse, game.mouse.cnt)
        self.tableBtn.drag(game.mouse.button,game.mouse.rect.topleft)
