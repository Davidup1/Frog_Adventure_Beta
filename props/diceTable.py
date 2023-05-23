from pygame.sprite import Group
from pygame.sprite import spritecollide
from props.table import Cell
from props.dice import Dice


class DiceTable:
    icon_dict = {}
    init_pos = (303, 462)

    def __init__(self, icon_dict):
        DiceTable.icon_dict = icon_dict
        self.cell_list = []
        self.cell_group = Group()
        pos = DiceTable.init_pos
        for i in range(5):
            cell = Cell(i, (pos[0]+78*i+18, pos[1]+18))
            self.cell_list.append(cell)
            self.cell_group.add(cell)
        self.dice_list = []
        self.dice_group = Group()
        self.dice_remain = 0
        self.icon_list = [0]*5
        self.icon_pos_list = [(0, 0)]*5
        self.energy = 0

    def round_init(self, bag):
        self.energy = 0
        for i in range(5-len(self.dice_list)):
            dice = bag.take_out_dice()
            dice.throw_dice()
            self.dice_list.append(dice)
            self.dice_group.add(dice)
        self.update_dice_pos()

    def update_dice_pos(self):
        pos = DiceTable.init_pos
        for i in range(len(self.dice_list)):
            self.dice_list[i].set_pos((pos[0]+78*i, pos[1]))

    def update_icon(self):
        index = 0
        self.icon_list = []
        self.icon_pos_list = []
        for dice in self.dice_list:
            self.icon_list.append(DiceTable.icon_dict[dice.type])
            pos = DiceTable.init_pos
            self.icon_pos_list.append((pos[0]+12+78*index, pos[1]+63))
            index += 1
        self.dice_remain = 0
        for i in self.dice_list:
            if i:
                self.dice_remain += 1
        self.energy = self.dice_remain-2

    def take_out_dice(self, dice):
        self.dice_list.remove(dice)
        self.dice_group.remove(dice)
        self.update_dice_pos()

    def eventHandle(self, game):
        mouse= game.mouse
        if mouse.button_up:
            if mouse.cur_dice and mouse.cur_dice.where != "diceTable":
                cells = spritecollide(mouse, self.cell_group, False)
                if cells:
                    index = self.cell_list.index(cells[0])
                    if index >= len(self.dice_list):
                        mouse.cur_dice.shift_place("diceTable")
                        self.dice_list.append(mouse.cur_dice)
                        self.dice_group.add(mouse.cur_dice)
                        self.update_dice_pos()

        for dice in self.dice_list:
            if not game.roundFinish:
                if dice.able != (self.energy != 0):
                    dice.able = (self.energy != 0)
                    dice.update_image()
