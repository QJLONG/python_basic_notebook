from socket import *

ip_port = ('127.0.0.1',8000)
buffer_size = 1024

# 创建socket链接 SOCK_DGRAM -> UDP协议
udp_server = socket(AF_INET,SOCK_DGRAM)

# 绑定IP，port
udp_server.bind(ip_port)

while True:
    try:
        # 接收消息
        data,addr = udp_server.recvfrom(buffer_size)
        print(data.decode('utf-8'),addr)
        if data.decode('utf-8') == 'exit':
            udp_server.sendto(data,addr)
            break
        # 发送消息
        msg = input('>>:')
        udp_server.sendto(msg.encode('utf-8'),addr)
    except Exception as e:
        print('程序出现异常，异常信息为：',e)
        break
# 关闭服务端
udp_server.close()