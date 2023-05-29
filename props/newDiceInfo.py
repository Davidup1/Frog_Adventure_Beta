from pygame.sprite import Sprite
from random import randint
from props.dice import Dice

types = ["ATTACK", "BLOCK", "BOOST", "HEAL", "MIRROR"]
specials = ["CRYSTAL", "HEAVY"]

class NewDiceInfo(Sprite):
    def __init__(self,cur_level):
        super(NewDiceInfo, self).__init__()
        self.dice = self.dice_generate()


    def dice_generate(self,cur_level):
        end = 3 if cur_level<7 else 4
        dice_type = types[randint(0,end)]
        num = cur_level//4
        dice_level = num if num<2 else 2
        dice_special = ""
        if dice_type=="HEAL":
            dice_special = specials[0] if cur_level<3 else ""
        if dice_type in ["ATTACK", "BLOCK","BOOST"]:
            dice_special = specials[1] if cur_level > 5 else ""
        return Dice(dice_type,dice_level,dice_special)

