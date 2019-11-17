from scapy.all import *
import sys

localmac = "b0:35:9f:21:5e:4e"
dstmac = "FF:FF:FF:FF:FF:FF"
localip = "192.168.1.103"
dstip = sys.argv[1]

result_raw = srp(Ether(dst = dstmac, src = localmac)/ARP(op=1, hwsrc=localmac, psrc=localip, pdst = dstip),iface="wlan0",verbose=False)
result = result_raw[0]
print(result.res[0][1].getlayer(ARP).fields['hwsrc'])