import sys
import pygame


def game_circulation(game):
    for event in pygame.event.get():
        # 关闭窗口
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def level_init(game):
    game.monsters = {}
    for i in game.level_data[str(int(game.cur_level/5))]['monsters']:
        pass
