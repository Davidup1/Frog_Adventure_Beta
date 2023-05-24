from socket import *

# 255.255.255.255表示向任何网段发送广播消息
address = ('255.255.255.255', 10130)

# 创建流式socket
s = socket(AF_INET, SOCK_DGRAM)

# 设置socket属性
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

message = b'This is broadcase message !'

# 发送广播消息
s.sendto(message, address)


print(' send ok !')

# 关闭socket
s.close()

