from socket import *

tcp_client = socket(AF_INET,SOCK_STREAM)

ip_port = ('127.0.0.1',8000)
buffer_size = 1024

tcp_client.connect(ip_port)
print('test-1')

while True:
    msg = input('>>:')
    if not msg: continue
    print('test-2')
    tcp_client.send(msg.encode('utf-8'))
    print('test-3')
    data = tcp_client.recv(1024)
    print(data)

tcp_client.close()
