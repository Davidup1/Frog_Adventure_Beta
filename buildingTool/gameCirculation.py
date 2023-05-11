import sys
import pygame


def game_circulation(game):
    game.mouse.click = False
    for event in pygame.event.get():  # ([clientData] if game.isFightMode else pygame.event.get())
        # 关闭窗口
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            game.mouse.rect.topleft = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.mouse.cnt += 1
            game.mouse.update_button(True)
        elif event.type == pygame.MOUSEBUTTONUP:
            game.mouse.update_button(False)
    game.mouse.update_button()

    if game.status == "main":
        for button in game.mainPage:
            button.eventHandle()
    if game.status == "level":
        level_page(game)
    game.mouse.log(game)


def level_page(game):
    if game.roundFinish:
        game.tableGroup.eventHandle(game)
        monster_movement(game)
    else:
        game.tableGroup.eventHandle(game)
        game.bag1.event_handle(game.mouse)
        game.bag2.event_handle(game.mouse)
        for dice in game.bag1.all_dices:
            dice.eventHandle(game.mouse)
        game.diceTable.eventHandle(game)
        if game.mouse.button_up:
            game.tableGroup.tableMain.calculate()







def monster_movement(game):
    if game.delay:
        game.delay -= 1
        if not game.delay:
            print("next")
    else:
        pass
