from socket import *
import subprocess
import struct

ip_port = ('127.0.0.1',8000)
back_log = 5
buffer_size = 1024

# 创建一个cmd_server 服务端
cmd_server = socket(AF_INET,SOCK_STREAM)

# 绑定端口ip
cmd_server.bind(ip_port)

# 设置最大监听数
cmd_server.listen(back_log)

# 设置外层循环，保证服务端持久运行
while True:
    # 建立连接
    conn,addr = cmd_server.accept()
    # 建立通信循环（内层循环）
    while True:
        try:
            # 接收客户端消息
            # -------------解决接收粘包----------------
            total_length = conn.recv(4)
            data_length = struct.unpack('i',total_length)[0]
            recv_size = 0
            recv_msg = b''
            while recv_size < data_length:
                recv_msg += conn.recv(buffer_size)
                recv_size = len(recv_msg)
            # -------------解决接收粘包----------------

            cmd = recv_msg.decode('utf-8')
            # 如果cmd命令为空 则断开连接
            if not cmd: break

            # 执行命令
            cmd_result = subprocess.Popen(cmd,shell=True,
                                          stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE)

            # 获取错误通道信息
            err_msg = cmd_result.stderr.read()

            # 如果错误通道有信息，返回客户端
            if err_msg:
                msg = err_msg
            # 如果错误通道没有信息，获取标准输出通道信息，并返回
            else:
                msg = cmd_result.stdout.read()
            # 如果命令正确，返回值为空
            if not msg:
                msg = '执行成功！'.encode('gbk')

            # 向客户端发型消息
            # -------------解决发送粘包---------------
            data_length = len(msg)
            total_length = struct.pack('i',data_length)
            conn.send(total_length)
            # -------------解决发送粘包---------------
            conn.send(msg)
        except Exception as e:
            print("程序出现异常：",e)
            break

    # 终端与客户端的链接
    conn.close()

# 关闭服务端
cmd_server.close()
