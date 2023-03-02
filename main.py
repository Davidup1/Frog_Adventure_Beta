import sys
import pygame
from buildingTool.imageLoading import imageLoading
from buildingTool.gameCirculation import gameCirculation


class Game():
    def __init__(self):
        filename = './image/bg_f1.png'
        pygame.init()
        pygame.display.set_caption("蛙蛙勇闯地牢")
        screen = pygame.display.set_mode((960, 539))
        imageLoading(screen, filename, (0, 0))

        while True:
            # 游戏内部循环中的事件处理
            gameCirculation(self)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()