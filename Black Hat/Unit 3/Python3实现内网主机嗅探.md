---
title: Python3实现内网主机嗅探
date: 2022-04-26 16:08:30
updated: 2022-04-26 16:08:30
categories: notebook
tags: python
urlname:
keywords: python3,socket
---

## Python3实现内网主机嗅探



### 嗅探原理

利用SOCKET_UDP向网段内所有IP的某一特殊端口发送UDP消息，这个特殊端口设置为不常用的端口，如果主机存活，就会向本机发送端口不可达(类型：3，代码值：3)ICMP报文，由此得知该主机存活



### 程序实现

1. 定义IP首部结构体，用于存放接收到的报文的IP首部信息

   ```python
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
           
   ```

   

2. 定义ICMP首部结构体，用于存放ICMP首部的信息

   ```python
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



3. 定义一个UDP数据包发送器，向网段中所有ip发送一条消息

   ```python
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
   ```

   

4. 定义一个数据包嗅探器，接收消息

   ```python
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
   ```



5. 设置线程开启消息发送器，并开始监听

   ```python
   if __name__ == '__main__':
       send_th = threading.Thread(target=udp_sender)
       send_th.start()
   
       sniffer_loop()
   ```

   