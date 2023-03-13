def show_info(game):
    fps_text = game.font.render(str(int(game.clock.get_fps())), False, (255,255,255))
    game.screen.blit(fps_text, (9, 0))

    game.game_frame_cnt += 1
    cnt_text = game.font.render(str(game.game_frame_cnt), False, (255, 255, 255))
    game.screen.blit(cnt_text, (9, 20))

    mouse_pos_text = game.font.render("%d,%d" % (game.mouse_pos[0], game.mouse_pos[1]), False, (255, 255, 255))
    game.screen.blit(mouse_pos_text, (36, 0))

    game_floor = game.font.render("Floor 1", False, (255, 255, 255))
    game.screen.blit(game_floor, (840, 0))
