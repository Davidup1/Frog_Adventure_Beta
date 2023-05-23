from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.sprite import collide_mask
from buildingTool.animation import Animation
from random import randint
from props.dice import Dice


class Bag(Sprite):
    images = {}

    def __init__(self, bag_type, images=None):
        super(Bag, self).__init__()
        if images:
            Bag.images = images
        self.bag_type = bag_type
        self.init_image = Bag.images["bag2" if bag_type else "bag1"].copy()
        self.hover_image = Bag.images["bag2_hover" if bag_type else "bag1_hover"].copy()
        self.image = self.init_image.copy()
        self.rect = self.image.get_rect()
        self.all_dices = Group()
        self.dice_list = []
        self.unable_list = []
        self.diceGroup = Group()
        self.remain = 0  # 剩余量
        self.position = (0, 0)
        self.mouseHover = False
        self.show_info = False
        self.init_info_image = Bag.images["bag_info"].copy()
        self.info_rect = self.init_info_image.get_rect()
        self.info_image = self.init_info_image.copy()
        if bag_type:
            self.rect.bottomright = (960, 539)
            self.info_rect.bottomright = (947, 395)
        else:
            self.rect.bottomleft = (0, 539)
            self.info_rect.bottomleft = (13, 395)
        self.info_animation = Animation()

    def init_dices(self, data):
        for i in data:
            dice = Dice(i[0], i[1], i[2])
            self.all_dices.add(dice)
            self.dice_list.append(dice)
            self.diceGroup.add(dice)
        self.init_info()
        self.remain = len(self.dice_list)

    def init_info(self):
        init_pos = (25, 78)
        cnt = 0
        for dice in self.dice_list:
            if dice.where == "bag":
                dice.set_pos((init_pos[0]+58*(cnt%6), init_pos[1]+58*(cnt//6)))
                dice.point = dice.pointList[-1]
                dice.update_image()
                cnt += 1

    def update_info(self):
        self.info_image = self.init_info_image.copy()
        self.diceGroup.draw(self.info_image)

    def on_mouse_hover(self, hover):
        if hover and not self.mouseHover:
            self.image = self.hover_image
        elif self.mouseHover and not hover:
            self.image = self.init_image
        self.mouseHover = hover

    def take_out_dice(self, dice=None):
        index = randint(0, self.remain - 1)
        self.dice_list[index].where = "diceTable"
        self.remain -= 1
        self.diceGroup.remove(self.dice_list[index])
        return self.dice_list.pop(index)

    def add_dice(self, dice):
        self.all_dices.add(dice)
        self.dice_list.append(dice)
        self.diceGroup.add(dice)
        pass

    def remove_dice(self, dice):
        self.all_dices.remove(dice)
        self.dice_list.remove(dice)
        self.diceGroup.remove(dice)
        pass

    def upgrade_dice(self, dice):
        dice.upgrade()
        pass

    def on_mouse_click(self, click):
        if self.mouseHover and click:
            self.show_info = not self.show_info
            size = self.init_info_image.get_rect().size
            size1 = self.info_rect.size
            if self.show_info:
                self.init_info()
                self.info_animation.scale(12, Animation.SIN, (int(size1[0]*0.01), int(size1[1]*0.01)), size)
            else:
                self.info_animation.scale(12, Animation.SIN, size1, (int(size[0]*0.01), int(size[1]*0.01)))
            self.info_animation.reset()

    def update_image(self):
        self.update_info()
        transformed_image = self.info_animation.play(self.info_image)
        if transformed_image:
            self.info_image = transformed_image
        self.info_rect = self.info_image.get_rect()
        if self.bag_type:
            self.rect.bottomright = (960, 539)
            self.info_rect.bottomright = (947, 395)
        else:
            self.rect.bottomleft = (0, 539)
            self.info_rect.bottomleft = (13, 395)

    def event_handle(self, mouse):
        self.on_mouse_hover(collide_mask(self, mouse))
        self.on_mouse_click(mouse.button_down)

    def round_reset(self,game):
        table = game.tableGroup.tableMain
        diceTable = game.diceTable
        for dice in self.all_dices:
            if dice.where != "bag":
                dice.able = True
                dice.update_image()
                if dice.where == "table":
                    if dice.special == "CRYSTAL":
                        dice.shift_place("bag")
                        self.unable_list.append(dice)
                    elif dice.special == "HEAVY":
                        dice.point -= 1
                    else:
                        self.dice_list.append(dice)
                        dice.shift_place("bag")
                        self.diceGroup.add(dice)
        self.remain = len(self.dice_list)
        diceTable.round_init(self)
        table.calculate(game)



