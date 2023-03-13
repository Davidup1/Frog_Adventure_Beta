import sys
from PIL import Image
import os
import pygame
from buildingTool.gameInit import game_init
from buildingTool.imageRendering import image_rendering
from buildingTool.gameCirculation import game_circulation
from buildingTool.gameCirculation import level_init


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load('./game_icon.png'))
        pygame.display.set_caption("蛙蛙勇闯地牢")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((960, 539))

        self.font = pygame.font.Font('./font/DinkieBitmap-7pxDemo.ttf', 21)
        self.game_frame_cnt = 0
        self.mouse_pos = (0, 0)
        self.cur_level = 1
        self.table_state = False  # 用于控制是否将棋盘收上去

        game_init(self)  # 加载了背景图片和游戏人物和怪物，并加载到列表
        level_init(self)  # 规定人物位置的方法

        while True:
            self.clock.tick(60)
            self.screen.fill((0,0,0))
            game_circulation(self)  # 游戏内部循环中的事件处理
            image_rendering(self)  # 游戏图像绘制
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
