from scapy.all import *
import struct


def ip_handle(src):
    src_list = src.split(".")
    for sec in src_list:
        src_pact = struct.pack(">B", int(sec))
        yield src_pact


def traceroute(src, dst):
    src_handle = ip_handle(src)
    ip_options = b'\x07\x27\x08'+next(src_handle)+next(src_handle)+next(src_handle)\
        +next(src_handle)+b'\x00'*33
    pkt = IP(dst = dst, options=IPOption(ip_options))/ICMP(type=8, code=0)
    result = sr1(pkt, timeout=60, verbose=False)
    # for router in result.getlayer(IP).options[0].fields['routers']:
    #     print(router)
    print(result.getlayer(IP).show())


traceroute("192.168.1.103","192.168.1.105")
