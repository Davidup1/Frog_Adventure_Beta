def show_fps(game):
    fps_text = game.font.render(str(int(game.clock.get_fps())), False, (255,255,255))
    game.screen.blit(fps_text, (9, 0))
    game.game_frame_cnt += 1
    cnt_text = game.font.render(str(game.game_frame_cnt), False, (255, 255, 255))
    game.screen.blit(cnt_text, (36, 0))
