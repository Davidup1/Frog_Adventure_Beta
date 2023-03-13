import pygame

class GameTable:
    def __init__(self, game, step, positionY=0):
        self.positionY = positionY
        self.maxPositionY = 384
        self.positionX = 400
        self.step = step
        self.tableFilePath = "../image/table/table_main.png"
        self.finishBtnFilePath = "../image/table/table_finish_button.png"
        self.tableImage = pygame.image.load(self.tableFilePath)
        self.finishBtn = pygame.image.load(self.finishBtnFilePath)


    def renderTable(self, positionY, game):
        # 用于棋盘上下移动
        if not game.table_state:
            pass
        else:
            pass