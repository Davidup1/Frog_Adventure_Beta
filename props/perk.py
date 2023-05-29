from buildingTool.animation import Animation
from pygame.sprite import Sprite
from pygame.sprite import collide_rect
from random import randint


class Perk(Sprite):
    def __init__(self,name,image):
        super(Perk, self).__init__()
        print(name)
        self.name = name
        self.image = image
        self.init_rect = self.image.get_rect()
        self.rect = self.init_rect.copy()
        self.animation = Animation()
        self.wait = 0
        self.mouseHover = False

    def set_pos(self,pos):
        self.init_rect.topleft = self.rect.topleft = pos

    def landing(self):
        self.animation.landing(30,-300,-300)
        self.wait = 60

    def selected(self,flag):
        if flag:
            self.animation.landing(15,30,0)
        else:
            self.animation.landing(15,-30,-30)

    def play(self):
        res = self.animation.play(self.init_rect)
        self.rect.topleft = res if res else self.rect.topleft

    def onMouseHover(self, game):
        hover = collide_rect(game.mouse, self)
        if self.wait:
            self.wait -= 1
        else:
            if hover:
                if not self.mouseHover:  # 移入
                    self.selected(1)
            else:
                if self.mouseHover:  # 移出
                    self.selected(0)
            self.mouseHover = hover

    def onClick(self,game):
        if self.mouseHover and game.mouse.button_down:
            if self.name == "healOrAddMaxHP":
                healOrAddMaxHP(game)
            elif self.name == "getNewDice":
                getNewDice(game)
            elif self.name == "removeDice":
                removeDice(game)
            elif self.name == "upgradeDice":
                upgradeDice(game)

    def eventHandle(self,game):
        self.onMouseHover(game)
        self.onClick(game)


def init_perks(img_dict):
    perk_dict = {}
    for i in img_dict.keys():
        perk_dict[i] = (Perk(i,img_dict[i]))
    return perk_dict


def gen_perk(perks):
    names = list(perks.keys())
    a = b = randint(0,len(perks)-1)
    while a==b:
        b = randint(0,len(perks)-1)
    perk1 = perks[names[a]]
    perk2 = perks[names[b]]
    perk1.set_pos((310,150))
    perk2.set_pos((500,150))
    return [perk1,perk2]


def healOrAddMaxHP(game):
    HP = game.player.balls["HP"]
    if HP.num == HP.MaxHP:
        HP.MaxHP += 3
    HP.num = HP.MaxHP
    game.next_level()


def getNewDice(game):

    pass


def removeDice(game):
    game.bag1.removeDice = True
    open_bag(game)
    print("removeDice")
    pass


def upgradeDice(game):
    game.bag1.upgradeDice = True
    open_bag(game)
    print("upgradeDice")
    pass

def open_bag(game):
    if not game.bag1.show_info:
        game.bag1.mouseHover = True
        game.bag1.on_mouse_click(True, game)
