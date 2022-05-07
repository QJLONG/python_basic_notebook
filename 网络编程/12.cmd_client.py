from socket import *
import struct

ip_port = ('127.0.0.1',8000)
back_log = 5
buffer_size = 2048

# 创建socket链接 tcp协议
cmd_client = socket(AF_INET,SOCK_STREAM)

# 建立连接
cmd_client.connect(ip_port)

# 实现循环通讯
while True:
    # 发送消息
    msg = input(">>:").strip()
    if not msg:continue
    # 如果中断连接，跳出循环
    if msg == 'exit':
        break
    cmd_client.send(msg.encode('utf-8'))

    # -----------------------解决粘包-----------------------
    length_data = cmd_client.recv(4) # 接收带有报头的字节流的长度
    length = struct.unpack('i',length_data)[0]  # 拆包 获取报文长度
    recv_size = 0
    recv_msg = b''
    while recv_size < length:    # 如果报文长度大于接收长度，则分组接收
        recv_msg += cmd_client.recv(300)
        recv_size = len(recv_msg)

    # -----------------------解决粘包 - --------------------

    # 接收消息
    print(recv_msg.decode('gbk'))

cmd_client.close()