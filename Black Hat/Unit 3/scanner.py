# -*- coding: utf-8 -*- 
# @Time : 2022/4/16 15:25 
# @Author : hummer 
# @File : sniffer_ip_header_decode.py

import socket
import os
import struct
import threading
import time
from netaddr import IPNetwork,IPAddress
from ctypes import *
import sys

# 监听的主机
host = "10.10.10.1"

subnet = "10.10.10.0/24"

# 自定义的字符串
magic_message = "HUMMER!"

# IP头定义
class IP(Structure):
    _fields_ = [
        ("ihl",c_ubyte,4),
        ("version",c_ubyte,4),
        ("tos",c_ubyte),
        ("len",c_ushort),
        ("id",c_ushort),
        ("offset",c_ushort),
        ("ttl",c_ubyte),
        ("protocol_num",c_ubyte),
        ("sum",c_ushort),
        ("src",c_ulong),
        ("dst",c_ulong)
    ]

    '''
        from_buffer_copy(source[, offset])
        此方法创建一个 ctypes 实例，从 source 对象缓冲区拷贝缓冲区，该对象必须是可读的。 
        可选的 offset 形参指定以字节表示的源缓冲区内偏移量；
        默认值为零。 如果源缓冲区不够大则会引发 ValueError。
    '''

    def __new__(self,socket_buffer=None):
        # 向_fileds_中读取数据，
        return self.from_buffer_copy(socket_buffer)

    def __init__(self,socket_buffer=None):

        # 协议字段与协议名称对应
        self.protocol_map = {1:"ICMP",6:"TCP",17:"UDP"}

        '''
            socket.inet_ntoa(packed_ip)
            将 32 位压缩 IPv4 地址（一个 类字节对象，长 4 个字节）转换为标准的点分十进制字符串形式（如 '123.45.67.89' ）。
            与那些使用标准 C 库，且需要 struct in_addr 类型的对象的程序交换信息时，本函数很有用。 
            该类型即本函数参数中的 32 位压缩二进制数据的 C 类型。
        '''

        # 可读的IP地址
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))

        # 协议类型
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    # 定义结构体
    _fields_ = [
        ("type",c_ubyte),
        ("code",c_ubyte),
        ("sum",c_short),
        ("unused",c_ushort),
        ("net_top_mtu",c_ushort)
    ]

    def __new__(self,icmp_buffer):
        return self.from_buffer_copy(icmp_buffer)

    def __init__(self,icmp_buffer):
        pass

# 批量发送数据包
def udp_sender(subnet,magic_message):
    time.sleep(5)

    sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message.encode('gbk'),("%s"%ip,65212))
        except Exception as e:
            print(e)




# 监听数据包
def sniffer_loop(host):
    global subnet
    global magic_message
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
    sniffer.bind((host,0))
    # 设置抓取的数据包包含IP首部
    sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

    if os.name ==  "nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

    while True:
        try:
            raw_buffer = sniffer.recvfrom(65565)[0]
            ip_header = IP(raw_buffer[0:20])
            offset = ip_header.ihl*4
            icmp_header = ICMP(raw_buffer[offset:offset+sizeof(ICMP)])

            if ip_header.protocol == "ICMP":

                print("Source: %s Type: %d Code: %d" % (ip_header.src_address,icmp_header.type,icmp_header.code))


                # 查看ICMP的类型和代码是否为3（端口不可达）
                if icmp_header.type == 3 and icmp_header.code == 3:

                    # 确认响应的主机在我们的目标子网内
                    if IPAddress(ip_header.src_address) in IPNetwork(subnet):

                        # # 确认数据包中包含我们的自定义字符
                        # if raw_buffer[len(raw_buffer)-len(magic_message):].decode('gbk') == magic_message:
                        print("Host Up: %s" % (ip_header.src_address))

        except KeyboardInterrupt:
            if os.name == "nt":
                sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)





def main():
    global subnet
    global magic_message
    global host

    t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
    t.start()
    # 开始监听
    sniffer_loop(host)
    # 开始发送数据包





if __name__ == '__main__':
    main()
