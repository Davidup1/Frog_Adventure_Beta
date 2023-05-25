import socket
from socket import *


address = ('255.255.255.255', 10130)
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while True:
    message = b'This is broadcase message from lyj !'
    s.sendto(message, address)

s.close()