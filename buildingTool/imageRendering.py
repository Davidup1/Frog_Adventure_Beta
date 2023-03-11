

def image_rendering(game):
    background_rendering(game)
    character_rendering(game)


def background_rendering(game):
    game.screen.blit(game.bg['bg'].gif(), (0, 0))
    game.screen.blit(game.bg['bg_fire'].gif(), (459, 0))


def character_rendering(game):
    game.screen.blit(game.player.gif.gif(), (game.player.x, game.player.y))
    for monster in game.monsters:
        pass


