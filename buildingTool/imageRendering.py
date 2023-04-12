from buildingTool.info import show_info


def image_rendering(game):
    background_rendering(game)
    character_rendering(game)
    game.tableGroup.draw(game.screen)
    game.bags.draw(game.screen)
    info_rendering(game)
    show_info(game)


def background_rendering(game):
    game.screen.blit(game.bg['bg'].gif(), (0, 0))
    game.screen.blit(game.bg['bg_fire'].gif(), (459, 0))


def character_rendering(game):
    game.screen.blit(game.player.gif.gif(), (game.player.x, game.player.y))  # 主角蛙蛙
    for monster in game.monsters:
        game.screen.blit(monster.gif.gif(), (monster.x, monster.y))  # 怪物


def info_rendering(game):
    game.bag1.update_image()
    if game.bag1.show_info or not game.bag1.info_animation.finish:
        game.screen.blit(game.bag1.info_image, game.bag1.info_rect)


def dice_rendering(game):
    pass

