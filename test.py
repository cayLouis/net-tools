from scapy.all import *

response = srp(Ether(src="b0:35:9f:21:5e:4e", dst="FF:FF:FF:FF:FF:FF")/ARP(op=1, hwsrc="b0:35:9f:21:5e:4e", psrc="192.168.1.103", pdst="192.168.1.1"),iface="wlan0",verbose=False)
print(response[0].res[0][1].getlayer(ARP).hwsrc)