import sys
import pygame
from random import randint


def game_circulation(game):
    for event in pygame.event.get():
        # 关闭窗口
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            game.mouse_pos = event.pos
            #print(game.mouse_pos)


def level_init(game):
    game.monsters = []
    level_data = game.level_data['level_stage'][str(int(game.cur_level/5))]
    level_pos = game.level_data['level_pos']
    monster_num = randint(1, level_data['monster_max'])
    monster_weight = level_data['monster_weight']
    for index in range(monster_num):
        random_num = randint(1, sum(monster_weight))
        weight = i = 0
        while i < len(monster_weight):
            weight += monster_weight[i]
            if random_num <= weight:
                break
        game.monsters.append(game.characters[level_data['monsters'][i]].copy(index+1, level_pos[monster_num-1][index]))
        print("name:%s index:%d pos:(%d,%d)" % (game.monsters[index].name, game.monsters[index].index, game.monsters[index].x, game.monsters[index].y))

