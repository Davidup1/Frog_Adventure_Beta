class Character:
    def __init__(self, name, gif, HP, pos_x, pos_y, index=0):
        self.name = name  # str
        self.gif = gif  # GifBuilder()
        self.cnt = 0
        self.index = index
        self.HP = HP  # int
        self.armour = 0
        self.ATK = 0
        self.x = self.init_x = pos_x  # int
        self.y = self.init_y = pos_y  # int
        self.size = gif.size

    def copy(self):
        self.cnt += 1
        return Character(
            self.name,
            self.gif.copy(),
            self.HP,
            self.x,
            self.y,
            self.cnt
        )

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]