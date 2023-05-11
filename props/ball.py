from buildingTool.animation import Animation


class Ball:
    img_dict = {}

    def __init__(self, ball_type="HP1", character_pos=None, img_dict=None, animation=None):
        if img_dict:
            Ball.img_dict = img_dict
        else:
            img_dict = Ball.img_dict
        self.type = ball_type
        self.img = img_dict[ball_type]
        self.character_pos = character_pos
        self.num = 0  # 数值
        self.animation = animation

    def update_image(self):
        pass

