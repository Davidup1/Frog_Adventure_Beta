from socket import *
import tkinter
import time

class NetConnection:
    def __init__(self):
        # 255.255.255.255表示向任何网段发送广播消息
        self.address = ('255.255.255.255', 10130)
        self.searchAddress = ('0.0.0.0', 10130)
        self.IP = self.getIP()

        # 创建流式socket
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.u = socket(AF_INET, SOCK_DGRAM)
        self.u.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.u.bind(self.searchAddress)
        self.u.settimeout(0.1)

    def popup(self):
        self.cnt = 0
        self.targetIP = "no user"
        self.page = tkinter.Tk()
        self.page.geometry("200x40+750+400")
        self.searchLabel = tkinter.Label(self.page, text="searching for user...", font=("微软雅黑", 14))
        self.searchLabel.pack()
        self.page.after(100, self.broadcast)
        self.page.mainloop()

    def getIP(self):
        import socket
        self.hostname = socket.gethostname()
        IP = socket.gethostbyname_ex(self.hostname)[2][0]
        return IP

    def broadcast(self):

        message = b'This is broadcase message from lyj !'
        self.s.sendto(message, self.address)
        try:
            self.search()
        except:
            pass
        print("send and recv")
        print(self.cnt)
        self.cnt += 1
        if self.cnt == 100:
            self.u.settimeout(1)
            try:
                self.search()
            except:
                pass
        else:
            self.page.after(100, self.broadcast)


    def search(self):
        print("wait recv...")
        count = 0
        while True:
            data, address = self.u.recvfrom(1024)
            if data == b"This is broadcase message from lyj !" and address[0]!= self.IP:
                self.targetIP = address[0]
                print(self.targetIP,time.time())
                break
        self.page.destroy()

    # def wait_for_connection(self,game):
    #     while True:
    #         data, address = self.s.recvfrom(1024)
    #         if data == b"This is broadcase message from lyj !" and address[0] != self.IP:
    #             game.server = address[0]
    #             print("作为从机")
    #             self.page.destroy()
    #             break


if __name__ == "__main__":
    s = NetConnection()