# Description: 
# Autor: hummer
# Date: 2022-04-24 20:40:50
# LastEditors: hummer
# LastEditTime: 2022-04-24 20:58:30


from ctypes import Structure, c_short, c_ubyte, c_ulong, c_ushort, sizeof
from glob import escape, glob
import threading
import time
from turtle import goto
from netaddr import IPAddress,IPNetwork
from socket import *
import os
import struct



# host = '172.21.92.140'
# subnet = "172.21.92.0/24"
host = '10.10.10.1'
subnet = '10.10.10.0/24'

# 自定义字符串
magic_message = "HUMMER!!!"

# IP头定义
class IP(Structure):
    _fields_ = [
        ("ihl",     c_ubyte,4),
        ("vesion",  c_ubyte,4),
        ("tos",     c_ubyte),
        ("len",     c_ushort),
        ("id",      c_ushort),
        ("off",     c_ushort),
        ("ttl",     c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum",     c_ushort),
        ("src",     c_ulong),
        ("dst",     c_ulong)
    ]
    
    def __new__(self,buffer=None):
        return self.from_buffer_copy(buffer)

    def __init__(self,buffer=None):
        
        # 解决协议号与协议对应问题
        self.protocol_map = {1:"ICMP",6:"TCP",17:"UDP"}
        

        # IP地址可读性
        self.src_address = inet_ntoa(struct.pack("<L",self.src))
        '''
            socket.inet_ntoa(packed_ip)
            将 32 位压缩 IPv4 地址（一个 类字节对象，长 4 个字节）
            转换为标准的点分十进制字符串形式（如 '123.45.67.89' )
        '''
        self.dst_address = inet_ntoa(struct.pack("<L",self.dst))

        # 协议类型处理
        try:
            if self.protocol_num in self.protocol_map:
                self.protocol = self.protocol_map[self.protocol_num]
            else:
                self.protocol = self.protocol_num
        except Exception as e:
            print(e)
        

class ICMP(Structure):
    _fields_ = [
        ("type",    c_ubyte),
        ("code",    c_ubyte),
        ("sum",     c_ushort),
        ("unused",  c_ushort),
        ("net_top_mtu",c_ushort)
    ]

    def __new__(self,buffer=None):
        return self.from_buffer_copy(buffer)
    
    def __init__(self,buffer=None):
        pass


def sniffer_loop():
    global subnet
    global host

    if os.name == 'nt':
        sock_protocol = IPPROTO_IP
    else:
        sock_protocol = IPPROTO_ICMP

    # 创建原始套接字
    socket_sniffer = socket(AF_INET,SOCK_RAW,sock_protocol)
    socket_sniffer.bind((host,0))

    # 设置包含IP头
    socket_sniffer.setsockopt(IPPROTO_IP,IP_HDRINCL,1)

    # 开启混杂模式
    if os.name == "nt":
        socket_sniffer.ioctl(SIO_RCVALL,RCVALL_ON)
    
    try:
        while True:
            socket_buffer = socket_sniffer.recvfrom(65565)[0]
            ip_header = IP(socket_buffer[0:20])
            offset = ip_header.ihl*4
            icmp_header = ICMP(socket_buffer[offset:offset+sizeof(ICMP)])

            # 判断src是否在子网内
            if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                
                if ip_header.protocol == "ICMP" and icmp_header.type == 3 and icmp_header.code == 3:
                    print("Protocol: %s %s->%s" % (ip_header.protocol,ip_header.src_address,ip_header.dst_address))
                    print("ICMP: %d %d" % (icmp_header.type,icmp_header.code))
    except Exception as e:
        if os.name == "nt":
            socket_sniffer.ioctl(SIO_RCVALL,RCVALL_OFF)
        print(e)


def udp_sender():
    global host
    global subnet

    time.sleep(5)
    udp_socket = socket(AF_INET,SOCK_DGRAM)
    udp_socket.bind((host,9999))
    
    # 向网段内所有主机发送UDP消息
    try:
        for host in IPNetwork(subnet):
            udp_socket.sendto(magic_message.encode('gbk'),(str(host),6666))
        
    except Exception as e:
        print(e)




if __name__ == '__main__':
    send_th = threading.Thread(target=udp_sender)
    send_th.start()

    sniffer_loop()