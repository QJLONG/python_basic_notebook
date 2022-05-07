from socket import *
import threading

ip_port = ('127.0.0.1',8000)
buffer_size = 1024
back_log = 5

# 创建一个server对象
tcp_server = socket(AF_INET, SOCK_STREAM)

# 绑定IP端口 设置最大监听shu
tcp_server.bind(ip_port)
tcp_server.listen(back_log)


def _server(conn):
    while True:
        data = conn.recv(buffer_size)
        print(data.decode('utf-8'))
        conn.send(data.upper())


if __name__ == '__main__':

    while True:
        conn,addr = tcp_server.accept()
        s = threading.Thread(target=_server,args=(conn,))
        s.start()


