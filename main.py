import sys
import pygame
from buildingTool.backgroundBuilding import backgroundBuilding
from buildingTool.imageLoading import imageLoading
from buildingTool.gameCirculation import gameCirculation


class Game():
    def __init__(self):
        bg_filename = [['./image/bg/bg_f1.png',[0,0]],['./image/bg/bg_f2.png',[0,0]]]
        fire_filename = [['./image/bg/bg_fire_f1.png',[0,0]],['./image/bg/bg_fire_f2.png',[0,0]],\
                         ['./image/bg/bg_fire_f3.png',[0,0]],['./image/bg/bg_fire_f4.png',[0,0]]]
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("蛙蛙勇闯地牢")
        self.screen = pygame.display.set_mode((960, 539))
        self.imageInit = imageLoading(bg_filename)
        self.fireInit = imageLoading(fire_filename)

        while True:
            backgroundBuilding(self)
            # 游戏内部循环中的事件处理
            gameCirculation(self)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()