import socket


server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

server.bind(('127.0.0.1', 8888))

server.listen(5)

conn, ip_addr = server.accept()
while True:
    res = conn.recv(1024)
    conn.send(res.decode('utf-8').upper().encode('utf-8'))
    print(ip_addr)
    if res.decode('utf-8') == 'quit:':
        break

conn.close()
server.close()