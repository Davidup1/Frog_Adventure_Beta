from buildingTool.animation import Animation
from props.ball import Ball

class Character:
    def __init__(self, name, gif, HP, pos_x, pos_y, action, is_player=False, index=0):
        self.name = name  # str
        self.gif = gif  # GifBuilder()
        self.cnt = 0
        self.index = index
        self.action = action
        self.delay = 0
        self.is_player = is_player
        self.balls = {}
        self.balls["HP"] = Ball("HP1" if is_player else "HP2", HP)
        self.balls["ARM"] = Ball("ARM", 0)
        self.balls["DEF"] = Ball("DEF", 0)
        self.balls["ATK"] = Ball("ATK", 0)
        self.balls["Heal"] = Ball("Heal", 0)
        self.rect = self.gif.frameList[0].get_rect()
        self.rect.topleft = pos_x, pos_y
        self.init_rect = self.rect.copy()
        self.size = gif.size
        self.animation = Animation()
        self.func = None
        self.para = None

    def init_ball(self):
        for ball in self.balls.values():
            ball.init(self.rect)

    def copy(self, is_player=False):
        self.cnt += 1
        pos = self.init_rect.topleft
        return Character(
            self.name,
            self.gif.copy(),
            self.balls["HP"].num,
            pos[0],
            pos[1],
            self.action,
            is_player,
            self.cnt
        )

    def set_pos(self, pos):
        self.init_rect.topleft = self.rect.topleft = pos

    def get_point(self, attribute):
        return self.balls[attribute].num

    def jump(self):
        self.animation.peak(10,20)
        self.animation.set_direction(1)
        self.animation.reset()

    def attack(self):
        self.animation.peak()
        self.animation.set_direction(3 if self.is_player else 2)
        self.animation.reset()

    def hit(self, atknum=0):
        if self.is_player:
            if self.balls["ARM"].num > atknum:
                self.balls["ARM"].num -= atknum
            else:
                self.balls["HP"].num -= atknum - self.balls["ARM"].num
                self.balls["ARM"].num = 0
                self.animation.shake()
                self.animation.set_direction(2)
                self.animation.reset()
        else:
            if self.balls["ARM"].num > self.balls["ATK"].num:
                self.balls["ARM"].num -= self.balls["ATK"].num
                self.balls["ATK"].num = 0
            else:
                self.balls["HP"].num -= self.balls["ATK"].num - self.balls["ARM"].num
                self.balls["ARM"].num = 0
                self.animation.shake()
                self.animation.set_direction(3)
                self.animation.reset()

    def add_arm(self, armnum=0):
        if self.is_player:
            self.balls["ARM"].num += self.balls["DEF"].num
            self.balls["DEF"].num = 0
        else:
            self.balls["ARM"].num += armnum

    def add_hp(self, healnum=0):
        to_max = self.balls["HP"].to_max_HP()
        self.balls["HP"].num_change()
        if self.is_player:
            self.balls["HP"].num += self.balls["Heal"].num if to_max > self.balls["Heal"].num else to_max
            self.balls["Heal"].num = 0
        else:
            self.balls["HP"].num += healnum if to_max > healnum else to_max

    def delay_func(self,func=None,para=None,delay=-1):
        if func:
            self.func = func
        if para:
            self.para = para
        if self.delay>0:
            self.delay -= 1
            delay = self.delay
        else:
            self.delay = delay
        if delay==0:
            self.func(self.para)

    def play(self):
        self.delay_func()
        pos = self.animation.play(self.init_rect)
        self.rect.topleft = pos if pos else self.rect.topleft


