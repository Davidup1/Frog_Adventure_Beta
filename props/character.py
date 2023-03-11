class Character:
    def __init__(self, name, gif, HP, pos_x, pos_y, index=0):
        self.name = name  # str
        self.index = index
        self.gif = gif  # GifBuilder()
        self.HP = HP  # int
        self.armour = 0
        self.ATK = 0
        self.x = self.init_x = pos_x  # int
        self.y = self.init_y = pos_y  # int
        self.size = gif.size

    def copy(self, index, pos=(0, 0)):
        x = pos[0]
        y = pos[1]
        return Character(
            self.name,
            self.gif.copy(),
            self.HP,
            x if x else self.x,
            y if y else self.y,
            index
        )
