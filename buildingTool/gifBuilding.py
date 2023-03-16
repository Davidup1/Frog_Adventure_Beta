

class GifBuilder:
    def __init__(self, frames, wait_time=1):
        self.frameList = []
        for i in frames:
            self.frameList.append(frames[i] if isinstance(i, str) else i)
            # 把目录和图片加入到frameList
        self.maxFrame = len(self.frameList)-1
        self.curFrame = 0
        self.wait = wait_time-1  # 5
        self.cnt = 0
        self.size = self.frameList[0].get_size()  # 获取图片尺寸

    def gif(self):  # 绘制图像时调用 返回当前帧对应图像
        if self.cnt == self.wait:  # 每 wait_time 帧 切换到下一张图像
            self.curFrame = 0 if self.curFrame == self.maxFrame else self.curFrame + 1
            self.cnt = 0
        else:
            self.cnt += 1
        return self.frameList[self.curFrame]

    def copy(self):
        return GifBuilder(self.frameList, self.wait)


