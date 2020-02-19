import sys

from scapy.all import *

# 本地mac地址
localmac = "b0:35:9f:21:5e:4e"
dstmac = "FF:FF:FF:FF:FF:FF"
localip = "192.168.100.8"
dstip = sys.argv[1]

def get_mac(dst_ip):

    # 使用数据链路层发包时需要指定接口，如iface = wlan0
    result_raw = srp(Ether(dst=dstmac, src=localmac) / ARP(op=1, hwsrc=localmac, psrc=localip, pdst=dst_ip), iface="wlan0",
                 verbose=False)
    result = result_raw[0]
    return result.res[0][1].getlayer(ARP).fileds['hwsrc']


if __name__ == "__main__":
    get_mac(dstip)