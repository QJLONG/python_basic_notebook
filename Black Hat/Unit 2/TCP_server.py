# -*- coding: utf-8 -*- 
# @Time : 2022/4/12 14:53 
# @Author : hummer 
# @File : TCP_server.py

from socket import *
import threading

bind_ip = '0.0.0.0'
bind_port = 9999
buffer_size = 4096

# 创建一个server对象
socket_server = socket(AF_INET,SOCK_STREAM)

# 绑定数据
socket_server.bind((bind_ip,bind_port))
socket_server.listen(5)
print("[*] Lintening on %s:%d" % (bind_ip,bind_port))

# client处理函数
def handle_client(client):

    # 实现通信循环
    while True:
        request = client.recv(buffer_size)
        if not request:
            continue
        request = request.decode()

        # 判断client是否exit
        if request == 'exit':
            print('[*] Connection disconnected!')
            client.close()
            break
        print("[*] Received: %s" % request)
        client.send("ACK!".encode())


while True:
    client,addr = socket_server.accept()
    print("[*] Accepted from: %s:%d" % (addr[0],addr[1]))
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
