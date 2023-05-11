from pygame.sprite import Sprite
from pygame.sprite import collide_rect
from pygame.draw import rect as draw_rect


class Button(Sprite):
    def __init__(self, img, pos, func, game):
        super(Button, self).__init__()
        self.init_image = img.copy()
        self.hover_image = img.copy()
        self.image = img.copy()
        self.rect = self.init_image.get_rect()
        draw_rect(self.image, (255, 255, 255, 30), self.rect)
        self.hover_image.blit(self.image,self.rect)
        self.image = self.init_image
        self.rect.center = pos
        self.func = func
        self.mouseHover = None
        self.game = game

    def onMouseHover(self, mouse):
        hover = collide_rect(self, mouse)
        if hover and not self.mouseHover:  # 鼠标在btn上
            self.image = self.hover_image
        elif self.mouseHover and not hover:
            self.image = self.init_image
        self.mouseHover = hover

    def onClick(self, mouse):
        if self.mouseHover and mouse.button_up:
            self.func(self.game)

    def eventHandle(self):
        self.onMouseHover(self.game.mouse)
        self.onClick(self.game.mouse)
