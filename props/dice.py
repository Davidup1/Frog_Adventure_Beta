class Dice():
    def __init__(self, type, img, level, is_heavy=False, is_crystal=False):
        self.pointList = [1, 1, 1, 1, 1, 1]  # 点数列表
        self.point = 1
        self.type = type  # "ATTACK" BLOCK BOOST HEAL MIRROR
        self.image = img.copy()
        self.level = level  # "BASIC" SILVER GOLD
        self.heavy = is_heavy
        self.crystal = is_crystal
