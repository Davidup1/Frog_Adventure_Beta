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


def game_init(game):
    img = load_img_dir('./image')
    # print(img)
    with open('./data/init_data.json') as f:
        data = json_load(f)
    with open('./data/level_data.json') as f:
        game.level_data = json_load(f)

    game.mouse = Mouse()
    game.bg = background_init(img['bg'])  # bg目录，内含bg和bg_fire
    game.characters = character_init(data['character'], img['character'])
    game.player = game.characters['frog']
    game.pointCard = PointCard(img["ball"]["point_card"], game.font)
    game.tableGroup = Table([img["table"]["table_main"], img["table"]["table_finish_button"]],game.pointCard)
    game.testDice = Dice(img_dict=img["dice"])  # 初始化骰子的图像到类里
    game.bag1 = Bag(0, img["bag"])
    game.bag1.init_dices(game.level_data["init_dices"]["level_mode"])
    game.bag2 = Bag(1)
    game.bags = Group()
    game.bags.add(game.bag1)
    game.bags.add(game.bag2)
    game.diceTable = DiceTable(img["diceTable"])


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
