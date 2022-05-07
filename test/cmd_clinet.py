from socket import *

ip_port = ('127.0.0.1',8000)
back_log = 5
buffer_size = 2048

# 创建一个cmd_server对象
cmd_client = socket(AF_INET,SOCK_STREAM)

# 与服务端建立连接
cmd_client.connect(ip_port)

# 实现通信循环
while True:
    # 向服务端发型cmd命令
    cmd = input('>>:')
    if not cmd: continue
    if cmd == 'exit':
        print('连接已断开。。。')
        break
    cmd_client.send(cmd.encode('utf-8'))

    # 接收服务端消息
    data = cmd_client.recv(buffer_size)
    if not data:
        break
    print(data.decode('gbk'))

cmd_client.close()
