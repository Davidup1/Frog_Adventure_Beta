class Character:
    def __init__(self, name, gif, HP, pos_x, pos_y):
        self.name = name  # str
        self.gif = gif  # GifBuilder()
        self.HP = HP  # int
        self.armour = 0
        self.ATK = 0
        self.x = self.init_x = pos_x  # int
        self.y = self.init_y = pos_y  # int
        self.size = (0, 0)
