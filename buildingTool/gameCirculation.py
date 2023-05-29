import sys
import pygame
from random import randint
from props.perk import gen_perk
import socket
from socket import *
import threading

def game_circulation(game):
    game.mouse.click = False
    for event in pygame.event.get():  # ([clientData] if game.isFightMode else pygame.event.get())
        # 关闭窗口
        if event.type == pygame.QUIT:
            if game.onlineClicked:
                game.threadControl = False
                game.onlineListen.join()
                pygame.quit()
                sys.exit()
            else:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            game.mouse.rect.topleft = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.mouse.cnt += 1
            game.mouse.update_button(True)
        elif event.type == pygame.MOUSEBUTTONUP:
            game.mouse.update_button(False)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                game.monsters[0].balls["HP"].death = True
    game.mouse.update_button()

    if game.status == "main":
        for button in game.mainPage:
            button.eventHandle()
    if game.status == "wait":
        pass
    if game.status == "level":
        level_page(game)
    if game.status == "online":
        online_page(game)
    game.mouse.log(game)


def level_page(game):
    # 清除死亡怪物
    for monster in game.monsters:
        if monster.balls["HP"].death:
            game.monsters.remove(monster)
            game.monster_num = len(game.monsters)
    if game.monster_num==0 and game.flag[0]=="monster" and not game.level_complete:# 战斗结束瞬间
        game.diceTable.clear_dice()
        game.tableGroup.tableMain.clear_dice()
        game.bag1.dice_back()
        game.temp_perk = gen_perk(game.perks)
        for perk in game.temp_perk:
            perk.landing()
    game.level_complete = game.monster_num==0 and game.flag[0]=="monster"
    if game.level_complete:  # 战斗结束
        choose_perk(game)
        game.bag1.event_handle(game)
        for dice in game.bag1.all_dices:
            dice.eventHandle(game.mouse)
    else:  # 战斗未结束
        if game.roundFinish:  # 回合结束
            game.tableGroup.eventHandle(game)
            character_movement(game)
        else:  # 回合未结束
            game.tableGroup.eventHandle(game)
            game.bag1.event_handle(game)
            for dice in game.bag1.all_dices:
                dice.eventHandle(game.mouse)
            game.diceTable.eventHandle(game)
            if game.mouse.button_up:
                game.tableGroup.tableMain.calculate(game)

def online_page(game):
    for monster in game.monsters:
        if monster.balls["HP"].death:
            game.monsters.remove(monster)
            game.monster_num = len(game.monsters)
    game.level_complete = game.monster_num==0
    if game.level_complete:  # 战斗结束
        win_online(game)
    else:  # 战斗未结束
        if game.roundFinish:  # 回合结束
            game.tableGroup.eventHandle(game)
            character_movement(game)
        else:  # 回合未结束
            game.tableGroup.eventHandle(game)
            game.bag1.event_handle(game)
            for dice in game.bag1.all_dices:
                dice.eventHandle(game.mouse)
            game.diceTable.eventHandle(game)
            if game.mouse.button_up:
                game.tableGroup.tableMain.calculate(game)

# 伤害数值
attacks = {"attack_s":(1,2),"attack":(1,3),"attack_b":(2,4),"attack_h":(4,7)}
# 防御数值
defences = {"defence":(1,3)}
# 治疗数值
heals = {"heal":(1,3)}


def character_movement(game):
    if game.delay:
        game.delay -= 1
        game.player.play()
        if len(game.monsters):
            game.monsters[game.cur_monster].play()
        if not game.delay:
            if game.flag == ["player", "attack"]:
                if game.monsters[-1].get_point("ATK"):
                    game.player.attack()
    else:
        if game.flag[0] == "player":
            if game.flag[1] == "attack":
                try:
                    if game.patch:
                        game.patch -= 1
                        game.player.play()
                        if game.patch==0:
                            game.flag[1] = "defence"
                            game.delay = 20
                    else:
                        if game.monsters[-1].get_point("ATK"):
                            game.player.play()
                            game.monsters[-1].play()
                            if game.player.animation.curFrame == len(game.player.animation.animationList)-1:
                                game.monsters[-1].hit()
                            if game.player.animation.finish:
                                game.monsters[-1].balls["ATK"].num = 0
                                game.delay = 20
                                game.flag[1] = "defence"
                        else:
                            game.flag[1] = "defence"
                except IndexError:
                    game.patch = 10
            elif game.flag[1] == "defence":
                if game.player.get_point("DEF"):
                    game.player.add_arm()
                    game.player.jump()
                    game.delay = 40
                else:
                    game.delay = 10
                game.flag[1] = "heal"
            elif game.flag[1] == "heal":
                if game.player.get_point("Heal"):
                    game.player.add_hp()
                    game.player.jump()
                    game.delay = 20
                game.flag = ["monster", "attack"]
                if len(game.monsters):
                    game.attack_flag = 1
                    actions = game.monsters[game.cur_monster].action
                    game.cur_actionlist = actions[randint(0,len(actions)-1)]
                    game.cur_action = 0
        elif game.flag[0] == "monster":
            if game.status == "online":
                # 写对手的动作
                if game.flag[1] == "attack":
                    game.player.play()
                    game.monsters[-1].play()
                    if not game.opponentAction["ATTACK"]:
                        game.player.hit()
                    if game.monsters[-1].animation.finish:
                        game.delay = 20
                        game.flag[1] = "defence"
                elif game.flag[1] == "defence":
                    if not game.opponentAction["BLOCK"]:
                        game.monsters[-1].add_arm()
                        game.monsters[-1].jump()
                        game.delay = 40
                    else:
                        game.delay = 10
                    game.flag[1] = "heal"
                elif game.flag[1] == "heal":
                    if not game.opponentAction["HEAL"]:
                        game.monsters[-1].add_hp()
                        game.monsters[-1].jump()
                        game.delay = 20
                    game.roundFinish = False
                    game.tableGroup.back()
                    game.bag1.round_reset(game)
            else:
                if game.cur_action < len(game.cur_actionlist):
                    action = game.cur_actionlist[game.cur_action]
                    monster = game.monsters[game.cur_monster]
                    if action in attacks.keys():
                        if game.attack_flag:
                            game.attack_flag = 0
                            monster.attack()
                        game.player.play()
                        monster.play()
                        if monster.animation.curFrame == len(monster.animation.animationList) - 1:
                            num = attacks[action]
                            game.player.hit(randint(num[0],num[1]))
                        if monster.animation.finish:
                            game.attack_flag = 1
                            game.delay = 10
                            game.cur_action += 1
                    elif action in defences.keys():
                        game.delay = 30
                        num = defences[action]
                        monster.jump()
                        monster_sel = game.monsters[randint(0,game.monster_num-1)]
                        para = randint(num[0],num[1])
                        monster_sel.delay_func(monster_sel.add_arm,para,15)
                        game.cur_action += 1
                    else:
                        game.delay = 30
                        num = heals[action]
                        monster.jump()
                        monster_sel = game.monsters[randint(0, game.monster_num - 1)]
                        para = randint(num[0], num[1])
                        monster_sel.delay_func(monster_sel.add_hp, para, 15)
                        game.cur_action += 1
                else:
                    game.cur_monster -= 1
                    if game.cur_monster >= -game.monster_num:
                        actions = game.monsters[game.cur_monster].action
                        game.cur_actionlist = actions[randint(0, len(actions) - 1)]
                        game.cur_action = 0
                    else:
                        game.roundFinish = False
                        game.cur_monster = -1
                        game.tableGroup.back()
                        game.bag1.round_reset(game)


def choose_perk(game):
    for perk in game.temp_perk:
        perk.eventHandle(game)
    pass

def win_online(game):
    pass
