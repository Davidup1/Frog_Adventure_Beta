from os import listdir
from json import load as json_load
from pygame.image import load as img_load
from buildingTool.gifBuilding import GifBuilder
from props.character import Character
from props.mouse import Mouse
from props.table import Table


def game_init(game):
    img = load_img_dir('./image')
    # print(img)
    with open('./data/init_data.json') as f:
        data = json_load(f)
        print(data)
    with open('./data/level_data.json') as f:
        game.level_data = json_load(f)
        print(game.level_data)

    game.mouse = Mouse()
    game.bg = background_init(img['bg'])  # bg目录，内含bg和bg_fire
    game.characters = character_init(data['character'], img['character'])  # {'frog': {'HP': 20, 'pos_x': 106, 'pos_y': 179, 'wait': 5}, 'fly_normal': {'HP': 6, 'pos_x': 704, 'pos_y': 179, 'wait': 7}, 'moth_normal': {'HP': 12, 'pos_x': 704, 'pos_y': 179, 'wait': 7}}
    # "fly_normal" "frog" "moth_normal"
    game.player = game.characters['frog']
    game.tableGroup = Table([img["table"]["table_main"],img["table"]["table_finish_button"]])



def background_init(img):
    background = {}
    for i in img:
        print(i)
        background[i] = GifBuilder(img[i], 6)  #传入"bg"和"bg_fire"
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
