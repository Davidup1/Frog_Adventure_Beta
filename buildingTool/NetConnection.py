import socket
from socket import *
import tkinter

class NetConnection:
    def __init__(self):
        # 255.255.255.255表示向任何网段发送广播消息
        self.address = ('255.255.255.255', 10130)
        self.searchAddress = ('0.0.0.0', 10130)

        # 创建流式socket
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.u = socket(AF_INET, SOCK_DGRAM)
        self.u.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.u.bind(self.searchAddress)
        self.u.settimeout(10)

        self.cnt = 0
        self.targetIP = "no user"
        self.page = tkinter.Tk()
        self.searchLabel = tkinter.Label(self.page, text="searching for user...")
        self.searchLabel.pack()
        self.page.after(100, self.broadcast)
        self.page.mainloop()

    def broadcast(self):

        message = b'This is broadcase message from lyj !'
        self.s.sendto(message, self.address)
        print("send")
        print(self.cnt)
        self.cnt += 1
        if self.cnt == 10:
            self.search()
        else:
            self.page.after(100, self.broadcast)


    def search(self):
        print("wait recv...")
        self.u.settimeout(10)
        count = 0
        while True:
            data, address = self.u.recvfrom(1024)
            if data == b"This is broadcase message from lyj !" and count == 0:
                tmpIP = address[0]
                print(tmpIP)
                count += 1
            if data == b"This is broadcase message from lyj !":
                self.targetIP = address[0]
                if self.targetIP != tmpIP:
                    break
        self.targetIP = address[0]
        print(self.targetIP)


if __name__ == "__main__":
    s = NetConnection()