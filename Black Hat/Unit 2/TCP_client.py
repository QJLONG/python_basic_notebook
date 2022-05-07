# -*- coding: utf-8 -*- 
# @Time : 2022/4/12 15:10 
# @Author : hummer 
# @File : TCP_client.py

from socket import *

target_ip = '127.0.0.1'
target_port = 9999
buffer_size = 4096

# 创建一个client对象
socket_client = socket(AF_INET,SOCK_STREAM)

# 与服务前建立连接
socket_client.connect((target_ip,target_port))
print("[*] Connected from: %s:%d" % (target_ip,target_port))

# 实现通信循环
while True:
    request = input('[*] Please input your request >>')
    socket_client.send(request.encode('utf-8'))

    # 判断client是否exit
    if request == 'exit':
        print('[*] Connection disconnected!')
        socket_client.close()
        break

    # 如果不退出，显示服务端response
    else:
        response = socket_client.recv(buffer_size)
        print('[*] Resived: %s' % response.decode('utf-8'))


