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

# 建立socket
tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 与服务端建立连接
tcp_client.connect(('127.0.0.1',8000))

buffer_size = 1024
# 通讯循环 实现与服务端循环交互
while True:
    try:
        # 发送消息
        msg = input('>>:')
        if not msg:
            msg = ' '

        # --------------解决发送端粘包问题---------------
        send_pack(msg,tcp_client)
        # --------------解决发送端粘包问题---------------
        tcp_client.send(msg.encode('utf-8'))

        # 接收消息
        # -------------解决接收端粘包问题------------
        recv_msg = recv_pack(tcp_client)
        # -------------解决接收端粘包问题------------

        if recv_msg.decode('utf-8') == 'exit':
            print('连接已断开。。。')
            send_pack(msg,tcp_client)
            tcp_client.send(recv_msg)
            break
        print('服务端说：',recv_msg.decode('utf-8'))
    except Exception as e:
        print(e)
# 断开与服务端的链接
tcp_client.close()