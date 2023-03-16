from buildingTool.info import show_info


def image_rendering(game):
    background_rendering(game)
    character_rendering(game)
    game.tableGroup.draw(game.screen)
    show_info(game)


def background_rendering(game):
    game.screen.blit(game.bg['bg'].gif(), (0, 0))
    game.screen.blit(game.bg['bg_fire'].gif(), (459, 0))


def character_rendering(game):
    game.screen.blit(game.player.gif.gif(), (game.player.x, game.player.y))  # 主角蛙蛙
    for monster in game.monsters:
        game.screen.blit(monster.gif.gif(), (monster.x, monster.y))  # 怪物

