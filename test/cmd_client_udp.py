from socket import *

ip_port = ('127.0.0.1',8000)
back_log = 5
buffer_szie = 2048

# 创建一个cmd_server的udp对象
cmd_client = socket(AF_INET,SOCK_DGRAM)

# 实现通信循环
while True:
    try:
        # 发送cmd命令给服务端
        cmd = input('>>:')
        # 如果输入命令为空
        if not cmd: continue
        # 输入exit退出循环
        if cmd == 'exit': break

        cmd_client.sendto(cmd.encode('utf-8'),ip_port)

        # 接收服务端信息
        data,addr = cmd_client.recvfrom(buffer_szie)
        print(data.decode('gbk'),addr)
    except Exception as e:
        print('程序出现异常，异常信息为：',e)
        break

cmd_client.close()
