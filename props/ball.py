
class Ball:
    img_dict = {}

    def __init__(self, ball_type, character_pos=None, img_dict=None):
        if img_dict:
            Ball.img_dict = img_dict
        else:
            img_dict = Ball.img_dict
        self.img = img_dict[ball_type]
        self.character_pos = character_pos
        self.num = 0  # 数值
