

class GifBuilder:
    def __init__(self, frames, wait_time=1):
        self.frameList = []
        for i in frames:
            self.frameList.append(frames[i] if isinstance(i, str) else i)
        self.maxFrame = len(self.frameList)-1
        self.curFrame = 0
        self.wait = wait_time-1
        self.cnt = 0
        self.size = self.frameList[0].get_size()

    def gif(self):
        if self.cnt == self.wait:
            self.curFrame = 0 if self.curFrame == self.maxFrame else self.curFrame+1
            self.cnt = 0
        else:
            self.cnt += 1
        return self.frameList[self.curFrame]

    def copy(self):
        return GifBuilder(self.frameList, self.wait)


