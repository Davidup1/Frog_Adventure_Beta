from socket import *

# IP地址为空表示接收任何网段的广播消息
address = ('0.0.0.0', 10130)

# 创建流式socket
s = socket(AF_INET, SOCK_DGRAM)

# 设置socket属性
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# 绑定本地ip地址和端口
s.bind(address)
s.settimeout(10)

print(' wait recv...')

# 接收消息
data, address = s.recvfrom(1024)

print(' [recv form %s:%d]:%s' % (address[0], address[1], data))

# 关闭socket
s.close()

