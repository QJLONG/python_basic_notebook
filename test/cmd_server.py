from socket import *
import subprocess

ip_port = ('127.0.0.1',8000)
back_log = 5
buffer_size = 1024

# 创建一个cmd_server对象
cmd_server = socket(AF_INET,SOCK_STREAM)

# 绑定ip端口
cmd_server.bind(ip_port)

# 设置最大监听数
cmd_server.listen(back_log)

# 实现外层循环，保证服务器一直启动
while True:
    # 建立连接
    conn,addr = cmd_server.accept()
    # 实现通信循环（内层循环）
    while True:
        try:
            # 接收客户端消息
            cmd = conn.recv(buffer_size)
            # 如果cmd为空 直接断开连接
            if not cmd: break

            # 执行cmd命令
            cmd_result = subprocess.Popen(cmd.decode('utf-8'),shell=True,
                                          stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE)
            # 获取错误通道信息
            err_msg = cmd_result.stderr.read()

            # 如果错误通道信息不为空，返回给客户端
            if err_msg:
                msg = err_msg
            # 如果错误通道信息为空，获取标准输出通道信息并返回给客户端
            else:
                msg = cmd_result.stdout.read()
            # 如果命令执行成功，返回结果为空
            if not msg:
                msg = '执行成功'.encode('gbk')

            conn.send(msg)
        except Exception as e:
            print('程序出现异常，异常信息为：',e)
            break
    conn.close()

cmd_server.close()


