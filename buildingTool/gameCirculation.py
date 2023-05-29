import sys
import pygame
from random import randint
from props.perk import gen_perk
import tkinter as tk
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
            elif event.key == pygame.K_b:
                game.cur_level += 3
            elif event.key == pygame.K_ESCAPE:
                game.threadControl = False
                if game.status == "online":
                    game.onlineListen.join()
                elif game.status == "level":
                    btn = game.tableGroup.tableBtn.animation
                    if btn.curFrame==len(btn.animationList)-1:
                        game.tableGroup.tableBtn.pack_up(game,True)
                game.status = "main"
                game.broadcast.sendto(b"My suitcase is moved, i don't play",(game.targetIP, 10131))
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
        game.delay = 0
        game.player.balls["DEF"].num = 0
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
    is_win = game.monsters[-1].balls["HP"].num <= 0
    game.level_complete = is_win or game.player.balls["HP"].num<=0

    if game.level_complete:  # 战斗结束
        win_online(game,is_win)
    else:  # 战斗未结束
        if game.roundFinish:
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
                # 写对手的动作----------------------------------------
                if game.opponentAction_changed[0]:
                    if game.opponentAction_changed[1]:
                        game.monsters[-1].attack()
                        game.opponentAction_changed[1] = False
                    if game.flag[1] == "attack":
                        print(game.opponentAction)
                        try:
                            if game.patch:
                                game.patch -= 1
                                game.monsters[-1].play()
                                if game.patch == 0:
                                    game.flag[1] = "defence"
                                    game.delay = 20
                            else:
                                print('game.opponentAction["ATTACK"]',game.opponentAction["ATTACK"])
                                if game.opponentAction["ATTACK"]:
                                    game.player.play()
                                    game.monsters[-1].play()
                                    if game.monsters[-1].animation.curFrame == len(game.monsters[-1].animation.animationList) - 1:
                                        game.player.hit(game.opponentAction["ATTACK"])
                                    if game.monsters[-1].animation.finish:
                                        game.opponentAction["ATTACK"] = 0
                                        game.delay = 20
                                        game.flag[1] = "defence"
                                else:
                                    game.flag[1] = "defence"
                        except IndexError:
                            game.patch = 10
                    elif game.flag[1] == "defence":
                        if game.opponentAction["BLOCK"]:
                            game.monsters[-1].add_arm(game.opponentAction["BLOCK"])
                            game.monsters[-1].jump()
                            game.delay = 40
                        else:
                            game.delay = 10
                        game.flag[1] = "heal"
                    elif game.flag[1] == "heal":
                        if game.opponentAction["HEAL"]:
                            game.monsters[-1].add_hp(game.opponentAction["HEAL"])
                            game.monsters[-1].jump()
                            game.delay = 20
                        game.flag[1] = "next"
                    elif game.flag[1] == "next":
                        game.roundFinish = False
                        game.opponentAction_changed[0] = False
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

def win_online(game,is_win):
    root = tk.Tk()
    r_w = 600
    r_h = 350
    s_w = root.winfo_screenwidth()
    s_h = root.winfo_screenheight()
    x = round((s_w - r_w) / 2)
    y = round((s_h - r_h) / 2)

    root.geometry('%dx%d+%d+%d' % (r_w, r_h, x, y))
    root.update()
    root.title("Error")
    frame1 = tk.Frame(root, bd=5)
    frame1.pack()
    label1 = tk.Label(frame1, text="你赢了！" if is_win else "你输了！", font=("微软雅黑",14))
    label1.pack()
    root.mainloop()

    game.status = "main"
    game.threadControl = False
    game.onlineListen.join()
    pass
