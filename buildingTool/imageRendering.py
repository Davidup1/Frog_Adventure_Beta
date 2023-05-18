from buildingTool.info import show_info


def image_rendering(game):
    background_rendering(game)

    if game.status == "main":
        game.mainPage.draw(game.screen) # Group.draw
    elif game.status == "level":
        character_rendering(game)
        table_rendering(game)
        bag_rendering(game)
        diceTable_rendering(game)
        info_rendering(game)
    elif game.status == "online":
        character_rendering(game)
        table_rendering(game)
        bag_rendering(game)
        diceTable_rendering(game)
        info_rendering(game)

    show_info(game)


def background_rendering(game):
    game.screen.blit(game.bg['bg'].gif(), (0, 0))
    game.screen.blit(game.bg['bg_fire'].gif(), (459, 0))


def character_rendering(game):
    game.screen.blit(game.player.gif.gif(), game.player.rect.topleft)  # 主角蛙蛙
    if game.status == "level":
        for monster in game.monsters:
            game.screen.blit(monster.gif.gif(), monster.rect.topleft)  # 怪物
    if game.status == "online":
        # 这里去game_init里面添加对手玩家
        pass


def table_rendering(game):
    game.tableGroup.draw(game.screen)
    for dice in game.tableGroup.tableMain.dice_list:
        if dice:
            game.screen.blit(dice.image, dice.rect.topleft)
    for i in range(9):
        cell = game.tableGroup.tableMain.cellList[i]
        pos = cell.rect.center
        if game.tableGroup.tableMain.calculate_list[i][0]:
            game.screen.blit(cell.pointCard.image, (pos[0]+12, pos[1]-12))


def info_rendering(game):
    game.bag1.update_image()
    if game.bag1.show_info or not game.bag1.info_animation.finish:
        game.screen.blit(game.bag1.info_image, game.bag1.info_rect)


def bag_rendering(game):
    game.bags.draw(game.screen)
    remain = str(game.bag1.remain)
    remain_text = game.font.render(remain, False, (255, 255, 255))
    rect = remain_text.get_rect()
    rect.center = (22, 462)
    game.screen.blit(remain_text, rect)


def diceTable_rendering(game):
    game.diceTable.dice_group.draw(game.screen)
    game.diceTable.update_icon()
    pos_list = game.diceTable.icon_pos_list
    index = 0
    for icon in game.diceTable.icon_list:
        game.screen.blit(icon, pos_list[index])
        index += 1
    energy = str(game.diceTable.energy)
    energy_text = game.font.render(energy, False, (0, 0, 0))
    rect = energy_text.get_rect()
    rect.center = (264, 521)
    game.screen.blit(energy_text, rect)

