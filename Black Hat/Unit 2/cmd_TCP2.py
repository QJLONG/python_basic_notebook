# -*- coding: utf-8 -*- 
# @Time : 2022/4/14 9:04 
# @Author : hummer 
# @File : cmd_TCP.py

import sys
import subprocess
import threading
from socket import *
import getopt


# 基础数据
listen = False
port = 0
target = ""


def usage():
    print("cmd_TCP_usage:")
    print("-l       --listen        -Listen on [host]:[port] for incomming connections")
    print("-t       --target        -Target host to listen on")
    print("-p       --port          -Target port to listen on")
    print("Example: ")
    print("cmd_TCP.py -l -p 6666")
    print("cmd_TCP.py -t 127.0.0.1 -p 6666")
    sys.exit(0)



def server_loop():
    server_socket = socket(AF_INET,SOCK_STREAM)
    bind_host = '127.0.0.1'
    bind_port = port
    server_socket.bind((bind_host,bind_port))
    print("[*] Listening on %s:%d......" % (bind_port,bind_port))

    # 开始监听循环
    try:
        while True:
            client_socket,addr =  server_socket.accept()
            print("[*] Accepted from connection %s:%d" % (addr[0],addr[1]))

            # 创建额外的线程处理连接的客户端
            client_threading = threading.Thread(target=client_handler,args=(client_socket,))
            client_threading.start()
    except Exception as e:
        print(e)


def run_command(client_buffer):
    # 去掉换行
    command = client_buffer.rstrip()
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except Exception as e:
        return e
    return output




def client_handler(client):

    # 向客户端发送回应
    client.send('[*] Connect successfully!'.encode("gbk"))

    # 接收客户端消息
    try:
        while True:

            client_buffer = ""

            while '\n' not in client_buffer:
                data = client.recv(1024)
                client_buffer += data.decode()

            # 执行命令并返回响应给客户端
            response = run_command(client_buffer)

            client.send(response)

    except Exception as e:
        print(e)
        client.close()




def main():
    global listen
    global port
    global target

    if not len(sys.argv[1:]):
        usage()

    # 命令行参数处理
    try:
        opt,args = getopt.getopt(sys.argv[1:],"lt:p:",["listen","target","port"])
    except getopt.GetoptError as e:
        print(e)
        usage()

    for o,a in opt:
        if o in ["-l","--listen"]:
            listen = True
        elif o in ["-t","--target"]:
            target = a
        elif o in ["-p","--port"]:
            port = int(a)
        else:
            print("Invalid Parameters!")

    # 如果目标是监听某个端口，则进入监听循环
    if listen:
        server_loop()

    else:
        client_sender((target,port))


def client_sender(target):
    client_scoket = socket(AF_INET,SOCK_STREAM)

    try:
        # 连接远程主机
        client_scoket.connect(target)
        print("[*] Connecting......")

        # 接收远程主机响应
        while True:
            response = ""
            data = ""

            while True:
                data = client_scoket.recv(4096)
                len_data = len(data)
                response += data.decode("gbk")
                if len_data < 4096:
                    break
            print(response)
            # 向远程主机发送请求：
            print("<HUMMER:#>",end="")
            request = sys.stdin.readline()
            client_scoket.send(request.encode())
    except Exception as e:
        print(e)
        client_scoket.close()


if __name__ == '__main__':
    main()