import sys
from PIL import Image
import os
import pygame
from buildingTool.gifBuilding import backgroundBuilding, characterBuilding
from buildingTool.imageLoading import imageLoading
from buildingTool.gameCirculation import gameCirculation


class Game():
    def __init__(self):
        self.backgroundPath = './image/bg'
        backgroundFile = self.loadFile(self.backgroundPath)
        bg_filename = backgroundFile[:2]
        fire_filename = backgroundFile[2:]
        self.characterPath = './image/character'
        characterFile = self.loadFile(self.characterPath)
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("蛙蛙勇闯地牢")
        self.screen = pygame.display.set_mode((960, 539))
        self.bgImageInit = imageLoading(bg_filename)
        self.fireInit = imageLoading(fire_filename)
        self.characterInit = imageLoading(characterFile)

        while True:
            backgroundBuilding(self)
            characterBuilding(self)
            # 游戏内部循环中的事件处理
            gameCirculation(self)
            pygame.display.update()


    def loadFile(self,path):
        images = []
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                filename = path + '/' + filename
                images.append(filename)
        return images

if __name__ == "__main__":
    game = Game()