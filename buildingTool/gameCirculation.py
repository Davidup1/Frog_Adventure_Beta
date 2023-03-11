import sys
import pygame


def game_circulation(game):
    for event in pygame.event.get():
        # 关闭窗口
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()