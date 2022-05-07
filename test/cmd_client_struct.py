from socket import *
import struct

ip_port = ('127.0.0.1',8000)
buffer_size = 1024

# 创建一个cmd_server 服务端
cmd_client = socket(AF_INET,SOCK_STREAM)

# 与服务端建立连接
cmd_client.connect(ip_port)

# 建立通信循环
while True:
    try:
        # 向服务端发送cmd命令
        cmd = input('>>:')
        if not cmd: continue
        if cmd == 'exit': break

        # -----------解决发送粘包------------
        data_length = len(cmd)
        total_length = struct.pack('i',data_length)
        cmd_client.send(total_length)
        # -----------解决发送粘包------------
        cmd_client.send(cmd.encode('utf-8'))

        # 接收服务端信息
        # -----------解决接收粘包------------
        total_length = cmd_client.recv(4)
        data_length = struct.unpack('i',total_length)[0]
        recv_size = 0
        recv_msg = b''
        while recv_size < data_length:
            recv_msg = cmd_client.recv(buffer_size)
            recv_size = len(recv_msg)
        # -----------解决接收粘包------------
        result = recv_msg.decode('gbk')
        print('执行结果：',result)
    except Exception as e:
        print('程序出现异常：',e)

# 断开连接
cmd_client.close()

