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
        self.end = self.duration - 1
        self.finish = True
        self.is_init = True
        self.direction = 0

    def set_circulation(self, count, mode):
        self.circulationMode = mode  # 0:顺序遍历 1:折返遍历
        self.circulationCount = count  # -1:无限循环
        self.circulationNum = count
        self.next = 1

    def set_direction(self, direction):
        '''

        :param direction: 0:up 1:down 2:left 3:right
        :return:
        '''
        self.direction = direction

    def scale(self, duration, mode, start_size, end_size):
        self.set_circulation(0, 0)
        self.type = "scale"
        self.duration = duration
        self.animationList = [0] * duration
        x = end_size[0] - start_size[0]
        y = end_size[1] - start_size[1]
        for i in range(duration):
            if mode == Animation.LINEAR:
                self.animationList[i] = (int(start_size[0] + x * i / duration), int(start_size[1] + y * i / duration))
            elif mode == Animation.SIN:
                self.animationList[i] = (int(start_size[0] + x * (-cos(pi * i / duration) + 1) / 2),
                                         int(start_size[1] + y * (-cos(pi * i / duration) + 1) / 2))

    def float(self, duration, amplitude):
        self.finish = False
        self.set_circulation(-1, 0)
        self.type = "float"
        self.duration = duration
        self.animationList = [0] * duration
        for i in range(duration):
            self.animationList[i] = round(amplitude * cos(pi * 2 * i / duration))

    def quadratic(self, duration, peak=(1, -1), x_end=3):
        self.finish = False
        self.set_circulation(0, 0)
        self.type = "quadratic"
        self.duration = duration
        self.animationList = [0] * duration
        a, b = peak
        k = -b / a ** 2
        for i in range(duration):
            self.animationList[i] = round(k * (i * x_end / (duration - 1) - a) ** 2 + b)
        self.reset()

    def peak(self, duration=20, peak=100):
        self.finish = False
        self.set_circulation(1, 1)
        self.type = "peak"
        self.duration = duration
        self.animationList = [0] * duration
        k = peak / 4 ** 5
        for i in range(duration):
            self.animationList[i] = round(k * (4 ** (i / (duration - 1) * 5)))
        self.reset()

    def shake(self, duration=10, amplitude=30):
        self.finish = False
        self.set_circulation(0, 0)
        self.type = "shake"
        self.duration = duration
        self.animationList = [0] * duration
        for i in range(duration):
            self.animationList[i] = round(amplitude * cos(pi * 8 * i / duration)*4**(-i*2 / duration))
        self.reset()

    def reset(self):
        self.circulationCount = self.circulationNum
        self.next = 1
        self.end = self.duration -1
        self.curFrame = 0
        self.is_init = False
        self.finish = False

    def backward(self):
        self.circulationCount = self.circulationNum
        self.next = -self.next
        self.end = self.duration - 1 if self.next == 1 else 0
        self.finish = False

    def play(self, data, mode=0):
        is_end = (self.curFrame == self.end) or self.is_init
        if self.circulationCount:
            if self.circulationMode:
                if is_end:
                    self.circulationCount -= 1
                    self.next = -self.next
                    self.end = self.duration - 1 if self.next == 1 else 0
                self.curFrame += self.next
            else:
                if self.curFrame == self.duration - 1:
                    self.circulationCount -= 1
                    self.curFrame = 0
                self.curFrame += self.next
        else:
            if is_end:
                self.finish = True
            else:
                self.curFrame += self.next
                self.finish = False
        # print((self.curFrame==self.duration-1 and self.next==1) ,(self.curFrame==0 and self.next==-1) , self.is_init)
        # print("cur:", self.curFrame, "cnt:", self.circulationCount, "finish:", self.finish)

        if not self.finish:
            self.finish = (self.curFrame == self.end) and not self.circulationCount
            if self.type == "scale":  # data为image
                return transform.scale(data.copy(), self.animationList[self.curFrame])
            elif self.type in ["float", "quadratic", "peak", "shake"]:  # data为rect
                pos = data.center if mode else data.topleft
                num = self.animationList[self.curFrame]
                return pos[0] + ( (num if self.direction%2 else -num) if self.direction // 2 else 0), \
                       pos[1] + (0 if self.direction // 2 else (-num if self.direction%2 else num) )
        return None
