from buildingTool.animation import Animation

class Character:
    def __init__(self, name, gif, HP, pos_x, pos_y, index=0):
        self.name = name  # str
        self.gif = gif  # GifBuilder()
        self.cnt = 0
        self.index = index
        self.HP = HP  # int
        self.armour = 0
        self.ATK = 0
        self.rect = self.gif.frameList[0].get_rect()
        self.rect.topleft = pos_x, pos_y
        self.init_rect = self.rect.copy()
        self.size = gif.size
        self.animation = Animation()
        self.animation.peak()
        self.animation.finish = True

    def copy(self):
        self.cnt += 1
        pos = self.init_rect.topleft
        return Character(
            self.name,
            self.gif.copy(),
            self.HP,
            pos[0],
            pos[1],
            self.cnt
        )

    def set_pos(self, pos):
        self.init_rect.topleft = self.rect.topleft = pos

    def attack(self):
        self.animation.peak()
        self.animation.reset()

    def play(self):
        self.rect.topleft = self.animation.play(self.init_rect)


