from buildingTool.animation import Animation


class Ball:
    img_dict = {}
    font = None

    def __init__(self, ball_type="HP1", num=0, img_dict=None, font=None):
        if img_dict:
            Ball.img_dict = img_dict
        else:
            img_dict = Ball.img_dict
        if font:
            Ball.font = font
        self.type = ball_type
        self.init_image = img_dict[ball_type].copy()
        self.image = self.init_image.copy()
        self.init_rect = self.init_image.get_rect()
        self.rect = self.init_rect.copy()
        self.blit_rect = self.init_rect.copy()
        self.num = num  # 数值
        self.pre_num = num
        self.appear = False
        self.fade = False
        self.show = False
        self.death = False
        self.MaxHP = num if ball_type in ['HP1', 'HP2'] else None
        self.animation_full = Animation()
        self.animation_temp = Animation()

    def init(self, rect):
        if self.type in ["HP1", "HP2"]:
            pos = rect.midtop
            print(pos)
            self.init_rect.center = (pos[0], pos[1]-30)
            self.animation_full.float(240, 3)
        elif self.type == "ARM":
            pos = rect.midtop
            self.init_rect.center = (pos[0]+25, pos[1])
            self.animation_full.float(240, 3)
        else:
            self.animation_full.float(120, 6)
            if self.type == "DEF":
                pos = rect.midbottom
                self.init_rect.center = (pos[0], pos[1])
            elif self.type == "ATK":
                pos = rect.center
                self.init_rect.center = (pos[0]-70, pos[1]+40)
            else:
                pos = rect.center
                self.init_rect.center = (pos[0]+70, pos[1]+40)

    def to_max_HP(self):
        return self.MaxHP - self.num if self.type in ['HP1', 'HP2'] else None

    def update_image(self):
        self.appear = (not self.pre_num) and self.num
        self.fade = (not self.num) and self.pre_num
        if (self.pre_num != self.num) and self.type in ["HP1","HP2","ARM"]:
            self.num_change()
        self.pre_num = self.num
        if self.appear:
            self.ball_appear()
        if self.fade:
            self.ball_fade()
            #self.ball_fade()
        self.show = self.num>0 or self.appear or self.fade or not self.animation_temp.finish
        if self.show:
            pos = self.animation_full.play(self.init_rect, 1)
            self.image = self.init_image.copy()
            a = self.type
            text = Ball.font.render(("+" if a in ["DEF","Heal"] else "-" if a=="ATK" else "")+str(self.num), False,
                    ((255,255,0) if self.num == self.MaxHP else (0,0,0)) if a in ["HP1", "HP2"] else (255,255,255))
            rect = text.get_rect()
            rect.center = self.blit_rect.center
            self.image.blit(text, rect.topleft)
            scaled_image = self.animation_temp.play(self.image)
            self.image = scaled_image if scaled_image else self.image
            self.rect = self.image.get_rect()
            if pos:
                self.rect.center = pos
        self.death = self.MaxHP and self.num<=0 and self.animation_temp.finish

    def num_change(self):
        size = self.init_rect.size
        self.animation_temp.scale(5,Animation.LINEAR,size,(round(size[0]*1.5),round(size[1]*1.5)))
        self.animation_temp.set_circulation(1,1)
        self.animation_temp.reset()

    def ball_appear(self):
        self.animation_temp.scale(10, Animation.LINEAR, (1,1), self.init_rect.size)
        self.animation_temp.reset()

    def ball_fade(self):
        self.animation_temp.scale(10, Animation.LINEAR, self.init_rect.size, (1, 1))
        self.animation_temp.reset()


