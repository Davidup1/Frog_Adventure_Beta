
class PointCard:
    base = None
    font = None

    def __init__(self, base=None, font = None):
        if base:
            PointCard.base = base
        else:
            base = PointCard.base
        if font:
            PointCard.font = font
        else:
            font = PointCard.font
        self.font = font
        self.base_image = base.copy()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

    def copy(self):
        return PointCard()

    def update_image(self, num):
        text = self.font.render(str(num), False, (255, 255, 255))
        rect = text.get_rect()
        pos = self.rect.center
        rect.center = pos[0]+1, pos[1]
        self.image = self.base_image.copy()
        self.image.blit(text, rect.topleft)


