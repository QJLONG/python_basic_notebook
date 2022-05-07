'''
Description: 
Autor: hummer
Date: 2022-04-27 21:02:04
LastEditors: hummer
LastEditTime: 2022-04-27 21:07:24
'''
from scapy.all import *

def packet_callback(packet):
    print(packet.show())

sniff(prn=packet_callback,count=1)
