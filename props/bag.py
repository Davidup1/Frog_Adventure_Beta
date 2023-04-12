from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.sprite import collide_mask
from buildingTool.animation import Animation
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
        self.dice_list = []
        self.diceGroup = Group()
        self.remain = 0  # 剩余量,每回合结束后计算一次
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
        j = 0
        for i in data:
            self.dice_list.append(Dice(i[0], i[1], i[2]))
            self.diceGroup.add(self.dice_list[j])
            j += 1
        self.init_info()

    def init_info(self):
        init_pos = (25, 78)
        cnt = 0
        for dice in self.dice_list:
            if dice.inBag:
                dice.rect.topleft = (init_pos[0]+58*(cnt%6), init_pos[1]+58*(cnt//6))
                dice.point = dice.pointList[-1]
                dice.update_image()
                cnt += 1

    def update_info(self):
        self.info_image = self.init_info_image.copy()
        self.diceGroup.draw(self.info_image)

    def on_mouse_hover(self, hover):
        if hover and not self.mouseHover:  # 鼠标在btn上
            self.image = self.hover_image
        elif self.mouseHover and not hover:
            self.image = self.init_image
        self.mouseHover = hover

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

    def event_handle(self, game):
        self.on_mouse_hover(collide_mask(self, game.mouse))
        self.on_mouse_click(game.mouse.click)



