

def image_rendering(game):
    game.screen.blit(game.bg.gif(), (0, 0))
    game.screen.blit(game.bg_fire.gif(), (459, 0))
    for characterName in game.character:
        mob = game.character[characterName]
        game.screen.blit(mob['gif'].gif(), (mob['pos'][0]+mob['offset_x'], mob['pos'][1]+mob['offset_y']))
