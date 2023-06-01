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
        self.removeDice = False
        self.upgradeDice = False


    def init_dices(self, data):
        self.all_dices = Group()
        self.dice_list = []
        self.diceGroup = Group()
        for i in data:
            dice = Dice(i[0], i[1], i[2])
            dice.set_point(5)
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
                if self.upgradeDice:
                    dice.able = False if dice.level==2 else True
                else:
                    dice.able = True
                dice.update_image()
                cnt += 1

    def update_info(self,game):
        self.info_image = self.init_info_image.copy()
        if game.mouse.cur_dice:
            dice = game.mouse.cur_dice
            cnt = 0
            for i in dice.pointList:
                self.info_image.blit(Bag.images["dice_info_point_"+str(i)],(30*cnt+103,337))
                if cnt==5:
                    self.info_image.blit(Bag.images["dice_info_point_selected"], (30 * dice.pointIndex + 103, 337))
                cnt += 1
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
        self.remain -= 1
        pass

    def upgrade_dice(self, dice):
        dice.upgrade()
        pass

    def on_mouse_click(self, click,game):
        dice = game.mouse.cur_dice
        if click:
            if self.mouseHover:
                self.show_info = not self.show_info
                size = self.init_info_image.get_rect().size
                if self.show_info:
                    self.init_info()
                    self.update_info(game)
                    self.info_animation.scale(12, Animation.SIN, (int(size[0]*0.01), int(size[1]*0.01)), size)
                else:
                    self.info_animation.scale(12, Animation.SIN, size, (int(size[0]*0.01), int(size[1]*0.01)))
                self.info_animation.reset()
            elif self.show_info and dice:
                if self.removeDice:
                    self.removeDice = False
                    self.remove_dice(dice)
                    self.show_info = False
                    size = self.init_info_image.get_rect().size
                    self.info_animation.scale(12, Animation.SIN, size, (int(size[0] * 0.01), int(size[1] * 0.01)))
                    game.mouse.cur_dice = None
                    game.next_level()
                elif self.upgradeDice:
                    if dice.able:
                        self.upgradeDice = False
                        self.upgrade_dice(dice)
                        self.init_info()
                        self.update_info(game)
                        self.show_info = False
                        size = self.init_info_image.get_rect().size
                        self.info_animation.scale(12, Animation.SIN, size, (int(size[0] * 0.01), int(size[1] * 0.01)))
                        game.mouse.cur_dice = None
                        game.next_level()

    def update_image(self,game):
        self.update_info(game)
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

    def event_handle(self, game):
        mouse = game.mouse
        self.on_mouse_hover(collide_mask(self, mouse))
        self.on_mouse_click(mouse.button_down,game)

    def round_reset(self,game):
        table = game.tableGroup.tableMain
        diceTable = game.diceTable
        for dice in self.all_dices:
            if dice.where != "bag":
                dice.able = True
                dice.update_image()
                if dice.where == "table":
                    if dice.special == "CRYSTAL":
                        dice.set_point(5)
                        dice.shift_place("bag")
                        self.unable_list.append(dice)
                    elif dice.special == "HEAVY":
                        dice.point -= 1
                    else:
                        self.dice_list.append(dice)
                        dice.set_point(5)
                        dice.shift_place("bag")
                        self.diceGroup.add(dice)
        self.remain = len(self.dice_list)
        diceTable.round_init(self)
        table.calculate(game)

    def dice_back(self):
        self.dice_list = []
        self.diceGroup = Group()
        for dice in self.all_dices:
            dice.able = True
            dice.set_point(5)
            dice.where = "bag"
            self.dice_list.append(dice)
            self.diceGroup.add(dice)
        self.remain = len(self.dice_list)



