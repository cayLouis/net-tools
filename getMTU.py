from scapy.all import *
import time
import re

"""
该程序用于获取目的ip路由的最小MTU值，防止IP包被分片
"""
"""
测试环境有限，可能因为路由过程中由于防火墙的作用，阻止了主机对“需要进行分片但设置了不分片比特”的差错控制报文
的接收，导致接收到的报文均为None
"""


def response(dst, mtu):
    # 设置填充数据大小，用mtu的值减去IP头部和ICMP头部的大小
    pyload = b'l' * (int(mtu) - 28)

    ping_one_reply = sr1(IP(dst=dst, flags="DF") / ICMP() / pyload, timeout=3, verbose=False)
    try:
        type_no = ping_one_reply.getlayer(ICMP).type
        code_no = ping_one_reply.getlayer(ICMP).code
        if type_no == 3 and code_no == 4:
            return 1, mtu
        elif type_no == 0 and code_no == 0:
            return 2, mtu
    except Exception as e:
        if re.match(".*NoneType.*", str(e)):
            return None


def discover_min_mtu(dst):
    mtu = 1000
    while True:
        result = response(dst, mtu)
        if result is None:
            print("目标%s不可达" % dst)
            break
        elif result[0] == 1:
            mtu = mtu - 10
            print("MTU: %s 测试不通过" % str(mtu))
        elif result[0] == 2:
            print("目标：%s 的最小MTU为：%s" % (dst, str(mtu)))
            break
        time.sleep(1)


if __name__ == "__main__":
    discover_min_mtu("183.232.231.172")
