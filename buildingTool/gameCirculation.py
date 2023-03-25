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
            game.mouse.rect.topleft = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 302 >= game.mouse_pos[0] >= 300 and 128 >= game.mouse_pos[1] >= 80:
                game.table_state = not game.table_state
    game.tableGroup.collisionDetection(game.mouse)

def level_init(game):
    game.monsters = []
    level_data = game.level_data['level_stage'][str(game.cur_level//5)]
    level_pos = game.level_data['level_pos']
    monster_num = randint(level_data['monster_min'], level_data['monster_max'])  # 生成当前关卡怪物总数
    monster_weight = level_data['monster_weight']
    # 生成当前关卡怪物
    for index in range(monster_num):
        random_num = randint(1, sum(monster_weight))
        weight = 0
        for i in range(len(monster_weight)):
            weight += monster_weight[i]
            if weight >= random_num:
                game.monsters.append(game.characters[level_data['monsters'][i]].copy())
                break
    # 按血量排序后重设怪物位置
    game.monsters.sort(key=lambda mob: mob.HP, reverse=True)
    for index, monster in enumerate(game.monsters):
        monster.set_pos(level_pos[monster_num - 1][index])
    # 按y轴位置升序排序以便绘制
    game.monsters.sort(key=lambda mob: mob.y)
