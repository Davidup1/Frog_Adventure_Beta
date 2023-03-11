from os import listdir
from json import load as json_load
from pygame.image import load as img_load
from buildingTool.gifBuilding import GifBuilder
from props.character import Character


def game_init(game):
    img = load_img_dir('./image')
    # print(img)
    with open('./data/init_data.json') as f:
        data = json_load(f)
    with open('./data/level_data.json') as f:
        game.level_data = json_load(f)

    game.bg = background_init(img['bg'])
    game.characters = character_init(data['character'], img['character'])
    game.player = game.characters['frog']


def background_init(img):
    background = {}
    for i in img:
        background[i] = GifBuilder(img[i], 6)
    return background


def character_init(data, img):
    characters = {}
    for characterName in img:
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
