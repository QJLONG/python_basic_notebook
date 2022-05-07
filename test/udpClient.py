from socket import *

ip_port = ('127.0.0.1',8000)
buffer_size = 1024

# 创建socket链接 SOCK_DGRAM -> UDP协议
udp_client = socket(AF_INET,SOCK_DGRAM)

while True:
    # try:
        # 发送消息
        msg = input('>>:')
        udp_client.sendto(msg.encode('utf-8'),ip_port)


        # 接收消息
        data,addr = udp_client.recvfrom(buffer_size)
        if data.decode('utf-8') == 'exit':
            udp_client.sendto(data,ip_port)
            break
        print(data.decode('utf-8'),addr)
    # except Exception as e:
    #     print('程序出现异常，异常信息为',e)
    #     break

udp_client.close()
