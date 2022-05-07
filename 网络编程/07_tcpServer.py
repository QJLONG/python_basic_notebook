import socket
import struct

# 创建方法 解决发送端粘包问题
def send_pack(msg,conn):
    length = len(msg)
    length_data = struct.pack('i', length)
    conn.send(length_data)

# 创建方法 解决接收端粘包问题
def recv_pack(conn):
    data_length = conn.recv(4)
    length = struct.unpack('i', data_length)[0]
    recv_size = 0
    recv_msg = b''
    while recv_size < length:
        recv_msg += conn.recv(buffer_size)
        recv_size = len(recv_msg)
    return recv_msg

# 建立socket链接 AF_INET是基于网络套接字家族，SOCK_STREAM是tcp协议
tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 声明服务端的IP和端口
tcp_server.bind(('127.0.0.1',8000))

back_log = 5
buffer_size = 1024

# 设置最大连接数
tcp_server.listen(back_log)

# 设置外层循环 保证服务端永久执行
while True:
    # 得到tcp链接 conn为链接对象  addr为对方地址
    conn,addr = tcp_server.accept()
    # print(conn,addr)

    # 通信循环 实现与客户端循环交互
    while True:
        try:
            # 接受客户端的消息
            # ---------------解决接收端粘包问题------------------
            recv_msg = recv_pack(conn)
            # ---------------解决接收端粘包问题------------------

            if not recv_msg: break
            if recv_msg.decode('utf-8') == 'exit':
                send_pack(recv_msg, conn)
                conn.send(recv_msg)
                print('链接已断开。。。')
                break
            print('客户端说：',recv_msg.decode('utf-8'))

            # 发送消息给客户端
            msg = input('>>:')
            if not msg:
                msg = ' '

            # --------------解决发送端粘包问题---------------
            send_pack(msg,conn)
            # --------------解决发送端粘包问题---------------
            conn.send(msg.encode('utf-8'))
        except Exception as e:
            print('程序出现异常，异常信息为：',e)
            break

    # 断开连接
    conn.close()

# 关闭服务
tcp_server.close()