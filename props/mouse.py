from pygame import Surface
from pygame.sprite import Sprite
from props.dice import Dice


class Mouse(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface((1, 1))
        self.rect = self.image.get_rect()
        self.button_pre = False
        self.button = False
        self.button_down = False
        self.button_up = False
        self.cur_dice = None
        self.cur_cell = None
        self.cnt = 0

    def update_button(self, cur_button=None):
        if cur_button is not None:
            self.button_pre = self.button
            self.button = cur_button
        else:
            self.button_down = self.button and not self.button_pre
            self.button_up = self.button_pre and not self.button
            self.button_pre = self.button

    def log(self, game):
        if game.status == "level":
            pass
        if self.button_up:
            print("mouse_click_count:", self.cnt)
            if self.cur_dice and 0:
                print(self.cur_dice.where)
            if game.status == "level":
                pass
            # print(Dice.places["table"].dice_list)
            # for i in game.monsters:
            #     print(i.rect.topleft)
