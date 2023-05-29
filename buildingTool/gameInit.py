import json
from os import listdir
from json import loads as json_loads
from json import load as json_load
from pygame.image import load as img_load
from pygame.sprite import Group

from buildingTool.NetConnection import NetConnection
from buildingTool.gifBuilding import GifBuilder
from props.character import Character
from props.mouse import Mouse
from props.table import Table
from props.bag import Bag
from props.diceTable import DiceTable
from props.dice import Dice
from props.pointCard import PointCard
from props.button import Button
from props.ball import Ball
from random import randint

import threading
from socket import *
from traceback import format_exc
import random


def game_init(game):
    img = load_img_dir('./image')
    # print(img)
    with open('./data/init_data.json') as f:
        data = json_load(f)
    with open('./data/level_data.json') as f:
        game.level_data = json_load(f)

    main_page_init(game,img)
    game.status = "main"
    game.mouse = Mouse()
    game.bg = background_init(img['bg'])  # bg目录，内含bg和bg_fire
    game.ball = Ball(img_dict=img["ball"], font=game.font)
    game.characters = character_init(data['character'], img['character'])
    game.player = game.characters['frog'].copy(True)
    game.pointCard = PointCard(img["ball"]["point_card"], game.font)
    game.tableGroup = Table([img["table"]["table_main"], img["table"]["table_finish_button"]], game.pointCard)
    game.testDice = Dice(img_dict=img["dice"])  # 初始化骰子的图像到类里
    game.bag1 = Bag(0, img["bag"])
    game.bag1.init_dices(game.level_data["init_dices"]["level_mode"])
    game.bag2 = Bag(1)
    game.bags = Group()
    game.bags.add(game.bag1)
    game.bags.add(game.bag2)
    game.diceTable = DiceTable(img["diceTable"])
    game.level_complete = False


    game.testDice.bind(game.bag1, game.tableGroup.tableMain, game.diceTable)


def background_init(img):
    background = {}
    for i in img:
        background[i] = GifBuilder(img[i], 6)  # 传入"bg"和"bg_fire"
    return background


def character_init(data, img):
    characters = {}
    print(img)
    print(data)
    for characterName in img.keys():  # "fly_normal" "frog" "moth_normal"
        characters[characterName] = Character(
            characterName,
            GifBuilder(img[characterName], data[characterName]['wait']),
            data[characterName]['HP'],
            data[characterName]['pos_x'],
            data[characterName]['pos_y'],
            data[characterName]['action']
        )
    return characters


def load_img_dir(path):
    img_group = {}
    for filename in listdir(path):
        temp = filename.split('.')
        if len(temp) == 1:
            img_group[temp[0]] = load_img_dir(path+'/'+temp[0])
        elif temp[1] == 'png':
            img_group[temp[0]] = img_load(path + '/' + filename)
    return img_group

# 创建按钮实例
def main_page_init(game,img):
    game.mainPage = Group()
    button_list = ["level", "online", "settings"]
    func_list = [level, online, settings]
    pos = (479,178)
    for index in range(3):
        i = button_list[index]
        game.mainPage.add(Button(img["UI"]["main"][i],(pos[0],pos[1]+60*index),func_list[index],game))

def level(game):
    game.status = "level"
    level_init(game, "init")

def online(game):
    game.status = "online"
    online_init(game, "online")

def settings(game):
    game.status = "settings"

def level_init(game, mode="none"):
    if mode == "init":
        game.cur_level = 1
    else:
        game.cur_level += 1
    game.roundFinish = False
    game.player.init_ball()
    game.monsters = []
    level_data = game.level_data['level_stage'][str(game.cur_level//5)]
    level_pos = game.level_data['level_pos']
    monster_num = 2# randint(level_data['monster_min'], level_data['monster_max'])  # 生成当前关卡怪物总数
    print(level_pos[monster_num - 1])
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
    game.monsters.sort(key=lambda mob: mob.balls["HP"].num, reverse=True)
    for index, monster in enumerate(game.monsters):
        monster.set_pos(tuple(level_pos[monster_num - 1][index]))
        monster.init_ball()
    # 按y轴位置升序排序以便绘制
    game.monsters.sort(key=lambda mob: mob.rect.topleft[1])
    round_init(game)
    game.flag = ["",""] # 控制角色动作流程
    game.monster_num = len(game.monsters)
    game.cur_monster = -1


def online_init(game, mode):
    game.onlineClicked = True
    game.search_win = NetConnection()
    game.targetIP = game.search_win.targetIP
    print("捕获到的IP:",game.targetIP)
    online_edge_init(game)
    game.onlineListen = threading.Thread(target=online_listen, args=(game, ))
    game.onlineListen.start()
    select_Server(game)
    print(game.onlineLeader)
    if mode == "online":
        game.cur_level = 1
    else:
        game.cur_level += 1
    game.roundFinish = False
    game.player.init_ball()
    level_pos = game.level_data['level_pos']
    game.monsters = [game.characters["frog_online"].copy()]
    game.monsters[0].set_pos(level_pos[0][0])
    game.monster_num = len(game.monsters)
    game.monsters[0].init_ball()
    game.flag = ["", ""]
    game.cur_monster = 0
    round_init(game)


def online_edge_init(game):
    game.broadcast = socket(AF_INET, SOCK_DGRAM)
    game.broadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    game.listener = socket(AF_INET, SOCK_DGRAM)
    game.listener.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    game.IP = gethostbyname_ex(gethostname())[2][0]
    game.listener.bind((game.IP, 10131))
    game.listener.settimeout(0.1)

def online_listen(game):
    while game.threadControl:
        try:
            data, address = game.listener.recvfrom(1024)
            if address[0] == game.targetIP:
                game.opponentAction = json_loads(data.decode('utf-8'))
                print(game.opponentAction)
                # game.tableGroup.tableMain.sum = game.opponentAction
        except Exception:
            pass
    pass

def select_Server(game):
    game.broadcast.sendto(json.dumps(str(game.search_win.cnt)).encode('utf-8'), (game.targetIP, 10131))
    while True:
        data, address = game.listener.recvfrom(1024)
        if address[0] == game.targetIP:
            tmp = json_loads(data.decode('utf-8'))
            print(tmp)
            if int(tmp) > game.search_win.cnt:
                game.onlineLeader = False
    pass

def round_init(game):
    game.diceTable.round_init(game.bag1)