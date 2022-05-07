import socket

# 创建一个socket_server
socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 绑定IP，端口
socket_server.bind(('127.0.0.1',8000))

# 设置最大链接数
back_log = 5
buffersize = 1024
socket_server.listen(back_log)

# 设置外层循环，保证服务器永久执行
while True:
    # 建立连接
    conn,addr = socket_server.accept()

    # 会话交互循环
    while True:
        # 接收消息
        try:
            data = conn.recv(buffersize)
            if not data: break
            if data.decode(('utf-8')) == 'exit':
                conn.send(data)
                print('链接已断开。。。')
                break
            print('客户端说：',data.decode('utf-8'))

            # 发送消息
            msg = input(">>:")
            if not msg:
                msg = ' '
            conn.send(msg.encode('utf-8'))
        except Exception as e:
            print('程序出现异常，异常信息为：',e)
            break

    # 关闭会话
    conn.close()

# 关闭服务器
socket_server.close()



