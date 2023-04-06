import socket

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

client.connect(('127.0.0.1', 8888))

while True:
    inputStream = input('>>>:').strip()
    client.send(inputStream.encode('utf-8'))
    res = client.recv(1024)
    print(res.decode('utf-8'))
    if inputStream == 'quit:':
        break

client.close()