# -*- coding: utf-8 -*- 
# @Time : 2022/4/16 15:25 
# @Author : hummer 
# @File : sniffer_ip_header_decode.py

import socket
import os
import struct
from ctypes import *

# 监听的主机
host = "10.10.10.1"

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






if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)

sniffer.bind((host,0))

# 设置抓取的数据包中包含IP头
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

try:
    while True:

        # 读取数据包
        raw_buffer = sniffer.recvfrom(65565)[0]


        # 将缓冲区的前20个字节解析
        ip_header = IP(raw_buffer[0:20])


        # 输出协议和通信双方IP地址
        print("Protocol: %s %s -> %s" % (ip_header.protocol,ip_header.src_address,ip_header.dst_address))

        if ip_header.protocol == "ICMP":

            # 计算icmp数据包开始的位置
            offset = ip_header.ihl * 4

            icmp_header = ICMP(raw_buffer[offset:offset+sizeof(ICMP)])

            print("ICMP -> Type: %d Code %d" % (icmp_header.type,icmp_header.code))

        # 处理CTRL-C
except KeyboardInterrupt:
    # 如果在Windows上运行，关闭混杂模式
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)


