import socket

# 创建socket_client对象
socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 建立连接
socket_client.connect(('127.0.0.1',8000))
buffer_size = 1024
# 循环交互处理
while True:
    # 发送消息
    msg = input('>>:')
    if not msg:
        msg = ' '
    socket_client.send(msg.encode('utf-8'))

    # 接收消息
    data = socket_client.recv(buffer_size)
    if data.decode('utf-8') == 'exit':
        socket_client.send(data)
        print('连接已断开。。。')
        break
    print('服务端说：',data.decode('utf-8'))



# 断开连接
socket_client.close()