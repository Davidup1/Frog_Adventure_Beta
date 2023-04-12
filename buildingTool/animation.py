from pygame import transform
from math import pi
from math import cos


class Animation:
    LINEAR = 0
    SIN = 1

    def __init__(self):
        self.img = None
        self.duration = 0
        self.animationList = []
        self.curFrame = 0
        self.type = None
        self.circulationMode = 0
        self.circulationCount = 0
        self.circulationNum = 0
        self.next = 1
        self.finish = True
        self.is_init = True

    def set_circulation(self, count, mode):
        self.circulationMode = mode  # 0:顺序遍历 1:折返遍历
        self.circulationCount = count  # -1:无限循环
        self.circulationNum = count
        self.next = 1

    def scale(self, duration, mode, start_size, end_size):
        self.set_circulation(0, 0)
        self.type = "scale"
        self.duration = duration
        self.animationList = [0] * duration
        x = end_size[0] - start_size[0]
        y = end_size[1] - start_size[1]
        for i in range(duration):
            if mode == Animation.LINEAR:
                self.animationList[i] = (int(start_size[0]+x*i/duration), int(start_size[1]+y*i/duration))
            elif mode == Animation.SIN:
                self.animationList[i] = (int(start_size[0]+x*(-cos(pi*i/duration)+1)/2), int(start_size[1]+y*(-cos(pi*i/duration)+1)/2))

    def float(self, duration, amplitude):
        self.finish = False
        self.set_circulation(-1, 0)
        self.type = "float"
        self.duration = duration
        self.animationList = [0] * duration
        for i in range(duration):
            self.animationList[i] = round(amplitude*cos(pi*2*i/duration))
        print(self.animationList)

    def reset(self):
        self.circulationCount = self.circulationNum
        self.next = 1
        self.curFrame = 0
        self.is_init = False
        self.finish = False

    def play(self, data):
        is_end = (self.curFrame==self.duration-1 and self.next==1) or (self.curFrame==0 and self.next==-1) or self.is_init
        if self.circulationCount:
            if self.circulationMode:
                if is_end:
                    self.circulationCount -= 1
                    self.next = -self.next
                self.curFrame += self.next
            else:
                if self.curFrame == self.duration-1:
                    self.circulationCount -= 1
                    self.curFrame = 0
                self.curFrame += self.next
        else:
            if is_end:
                self.finish = True
            else:
                self.finish = False
                self.curFrame += self.next
        # print((self.curFrame==self.duration-1 and self.next==1) ,(self.curFrame==0 and self.next==-1) , self.is_init)
        # print("cur:", self.curFrame, "cnt:", self.circulationCount, "finish:", self.finish)

        if not self.finish:
            if self.type == "scale":  # data为image
                return transform.scale(data, self.animationList[self.curFrame])
            elif self.type == "float":  # data为rect
                pos = data.topleft
                return pos[0], pos[1]+self.animationList[self.curFrame]
        return None
