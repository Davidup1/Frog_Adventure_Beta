import pygame
from buildingTool.gameInit import game_init
from buildingTool.imageRendering import image_rendering
from buildingTool.gameCirculation import game_circulation
from buildingTool.info import show_info
from traceback import format_exc
import tkinter as tk
import time


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load('./game_icon.png'))
        pygame.display.set_caption("蛙蛙勇闯地牢")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((960, 539))

        self.font = pygame.font.Font('./font/寒蝉点阵体.ttf', 23)
        self.game_frame_cnt = 0
        self.cur_level = None
        self.delay = 0
        self.selfAction = {"ATTACK": 0, "BLOCK": 0, "HEAL": 0}
        self.opponentAction = {"ATTACK": 0, "BLOCK": 0, "HEAL": 0}
        self.onlineClicked = False
        self.threadControl = True
        self.onlineLeader = True
        try:
            game_init(self)

            while True:
                self.clock.tick(60)
                image_rendering(self)  # 游戏图像绘制
                game_circulation(self)  # 游戏内部循环中的事件处理
                show_info(self)
                pygame.display.update()

        except Exception:
            ErrorMessage = '='*12+time.asctime( time.localtime(time.time()) )+'='*12+'\n\n'
            ErrorMessage += format_exc()+'\n\n\n\n'
            with open('ErrorReport.txt', "a") as report:
                report.write(ErrorMessage)

            root = tk.Tk()
            r_w = 600
            r_h = 350
            s_w = root.winfo_screenwidth()
            s_h = root.winfo_screenheight()
            x = round((s_w-r_w)/2)
            y = round((s_h-r_h)/2)

            root.geometry('%dx%d+%d+%d' % (r_w, r_h, x, y))
            root.update()
            root.title("Error")
            frame1 = tk.Frame(root, bd=5)
            frame1.pack()
            label1 = tk.Label(frame1, text="程序运行出错，错误信息如下(已写入ErrorReport.txt)：")
            label1.pack()
            edit1 = tk.Text(frame1,  # 创建多行文本框
                                 selectbackground='red',  # 设置选中文本的背景色
                                 selectforeground='white')
            edit1.insert("0.0", ErrorMessage)
            edit1.pack()
            root.mainloop()



if __name__ == "__main__":
    game = Game()