import sys
from PIL import Image
import os
import pygame
from buildingTool.fps import show_fps
from buildingTool.gameImageInit import game_image_init
from buildingTool.imageRendering import image_rendering
from buildingTool.gameCirculation import game_circulation


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load('./game_icon.png'))
        pygame.display.set_caption("蛙蛙勇闯地牢")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((960, 539), pygame.RESIZABLE)
        # print(self.screen.get_size())

        self.font = pygame.font.Font('./font/DinkieBitmap-7pxDemo.ttf', 21)
        self.game_frame_cnt = 0

        game_image_init(self)

        while True:
            self.clock.tick(60)
            self.screen.fill((0,0,0))
            game_circulation(self)  # 游戏内部循环中的事件处理
            image_rendering(self)  # 游戏图像绘制
            show_fps(self)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
