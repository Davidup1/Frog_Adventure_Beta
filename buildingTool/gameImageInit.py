from os import listdir
from pygame.image import load
from buildingTool.gifBuilding import GifBuilder


def game_image_init(game):
    img = load_img_dir('./image')
    # print(game.img)
    game.bg = GifBuilder(img['bg']['bg'], 6)
    game.bg_fire = GifBuilder(img['bg']['bg_fire'], 6)
    game.character = {}
    for characterName in img['character']:
        game.character[characterName] = {
            'gif': GifBuilder(img['character'][characterName], 6),
            'pos': (106, 179),
            'offset_x': 0,
            'offset_y': 0
        }


def load_img_dir(path):
    img_group = {}
    for filename in listdir(path):
        temp = filename.split('.')
        if len(temp) == 1:
            img_group[temp[0]] = load_img_dir(path+'/'+temp[0])
        elif temp[1] == 'png':
            img_group[temp[0]] = load(path + '/' + filename)
    return img_group
