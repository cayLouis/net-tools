from scapy.all import *
import struct

"""
该程序用于测试源站路由
源站路由分为宽松源站路由和严格源站路由
因为实验环境有限，仅测试宽松源站路由，但两者原理差不多
"""


def send_route(dst, hop1, op):
    # 处理真实目的主机
    ip_sec = dst.split('.')
    sec_1 = struct.pack('>B', int(ip_sec[0]))
    sec_2 = struct.pack('>B', int(ip_sec[1]))
    sec_3 = struct.pack('>B', int(ip_sec[2]))
    sec_4 = struct.pack('>B', int(ip_sec[3]))
    # 以b开头的字符串表示字节字符串，是以字节来存储的
    option_data = b'\x83\x07\x04' + sec_1 + sec_2 + sec_3 + sec_4 + b'\x00'
    # 使用ICMP协议进行源站路由测试
    if op == 1:
        pkt = IP(dst=hop1, options=IPOption(option_data)) / ICMP(type=8, code=0)
        result = sr1(pkt, timeout=1, verbose=True)
    # 使用TCP协议进行源站路由测试
    elif op == 2:
        # 这里需要特别注意一下！！！
        """
        使用TCP构造包时，TCP会有校验码，这个校验码是根据TCP头部和数据以及伪TCP头部（IP头部）计算的,
        若真实的接收方检查校验码不一致，会自动丢弃。
        在scapy中TCP校验码是根据你造包时实际填入的目的ip地址（第一跳）计算的，所以真实的接收方会检测
        到校验码不对而丢弃该报文。可利用wireshark纠正后填入
        """
        pkt = IP(dst=hop1, options=IPOption(option_data)) / TCP(chksum=0xebde, sport=8088, dport=80)
        result = sr1(pkt, timeout=1, verbose=True)


send_route('192.168.1.100', '192.168.1.1', 2)
