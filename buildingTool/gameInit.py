from os import listdir
from json import load as json_load
from pygame.image import load as img_load
from pygame.sprite import Group
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
    game.characters = character_init(data['character'], img['character'])  # 游戏人物角色字典
    game.player = game.characters['frog']
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
    game.ball = Ball(img_dict=img["ball"])


    game.testDice.bind(game.bag1, game.tableGroup.tableMain, game.diceTable)


def background_init(img):
    background = {}
    for i in img:
        background[i] = GifBuilder(img[i], 6)  # 传入"bg"和"bg_fire"
    return background


def character_init(data, img):
    characters = {}
    for characterName in img:  # "fly_normal" "frog" "moth_normal"
        characters[characterName] = Character(
            characterName,
            GifBuilder(img[characterName], data[characterName]['wait']),
            data[characterName]['HP'],
            data[characterName]['pos_x'],
            data[characterName]['pos_y']
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
    online_init(game, "init")

def settings(game):
    game.status = "settings"

def level_init(game, mode):
    if mode == "init":
        game.cur_level = 1
    else:
        game.cur_level += 1
    game.roundFinish = False
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
    game.monsters.sort(key=lambda mob: mob.rect.topleft[1])
    round_init(game)

def online_init(game, mode):
    if mode == "init":
        game.cur_level = 1
    else:
        game.cur_level += 1
    game.roundFinish = False
    level_pos = game.level_data['level_pos']
    game.monsters = [game.characters["frog_online"].copy()]
    print(game.monsters[0].rect.topleft)
    game.monsters[0].set_pos(level_pos[0][0])
    print(game.monsters[0].rect.topleft)
    round_init(game)

def round_init(game):
    game.diceTable.round_init(game.bag1)