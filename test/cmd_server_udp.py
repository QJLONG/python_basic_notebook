from socket import *
import subprocess

ip_port = ('127.0.0.1',8000)

buffer_szie = 1024

# 创建一个cmd_server的udp对象
cmd_server = socket(AF_INET,SOCK_DGRAM)

# 绑定ip_port
cmd_server.bind(ip_port)


# 实现通信循环
while True:
    try:
        # 接收客户端的cmd命令
        cmd,addr = cmd_server.recvfrom(buffer_szie)
        # 如果命令为空
        if not cmd:
            pass
        print('客户端的命令为：',cmd.decode('utf-8'),addr)

        # 执行cmd命令
        cmd_result = subprocess.Popen(cmd.decode('utf-8'),shell=True,
                                      stderr=subprocess.PIPE,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)

        # 获取错误通道信息
        err_msg = cmd_result.stderr.read()
        # 如果错误通道信息不为空 返回给客户端
        if err_msg:
            msg = err_msg
        # 如果错误通道信息为空，获取标准输出通道信息
        else:
            msg = cmd_result.stdout.read()
        # 如果客户端输入的命令正确，但是标准输出通道的信息为空
        if not msg:
            msg = '执行成功！'.encode('gbk')
        # 将信息发送给客户端
        cmd_server.sendto(msg,addr)
    except Exception as e:
        print('程序出现异常，异常信息为：',e)
        break

# 关闭服务器
cmd_server.close()

