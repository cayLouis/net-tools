"""
该文件用于模拟 traceroute 命令，记录目的主机的路由
"""
# 导入需要用到的模块
from scapy.all import *
import time


def response(ip, dport, ttl):
    """

    :param ip: 需要记录路由的目的IP地址
    :param dport: 目的端口
    :param ttl: time to live
    :return: 收到的报文类型
    """
    # 记录发送报文时的时间戳
    send_time = time.time()
    # 发送构造的报文
    resp = sr1(IP(dst=ip, ttl=ttl)/UDP(dport=dport), verbose=False, timeout=1)
    # 监测未收到包的情况
    try:
        # 提取ICMP报文的类型和状态码
        type_no = resp.getlayer(ICMP).type
        code_no = resp.getlayer(ICMP).code
        # 判断ICMP报文是否为超时报文
        if type_no == 11 and code_no == 0:
            # 提取报文中的源IP地址
            psrc = resp.getlayer(IP).src
            # 记录接收到报文的时间戳
            recv_time = time.time()
            # 记录从发送到接收到报文所用的时间
            time_passed = (recv_time - send_time) * 1000
            # 返回数据
            return 1, psrc, time_passed
        # 判断ICMP报文是否为为端口不可达报文
        elif type_no == 3 and code_no == 3:
            # 提取报文中的源IP地址
            psrc = resp.getlayer(IP).src
            recv_time = time.time()
            time_passed = (recv_time - send_time) * 1000
            return 2, psrc, time_passed
    # 处理异常
    except Exception as e:
        if re.match('.*NoneType.*', str(e)):
            return None


def start_trace(dst, hops):
    """

    :param dst: 需要跟踪路由的目的主机
    :param hops: 最大跳数
    :return: None
    """
    # 设置目的端口
    dport = 24536
    # 初始化跳数
    hop = 0
    while hop < hops:
        # 设置目的端口
        dport = dport + hop
        # 每一次发送，跳数加1
        hop += 1
        # 判断接收到的报文类型，并得到相应的参数
        result = response(dst, dport, hop)
        # 如果没有收到返回的报文
        if result is None:
            print(str(hop) + ' *', flush=True)
        # 如果接收到的报文为超时报文
        elif result[0] == 1:
            time_to_pass = '%4.2f' % result[2]
            print(str(hop) + ' ' + str(result[1]) + ' ' + time_to_pass)
        # 如果接收到的报文为端口不可达报文
        elif result[0] == 2:
            time_to_pass = '%4.2f' % result[2]
            print(str(hop) + ' ' + str(result[1]) + ' ' + time_to_pass)
            # 已经到达目的主机，退出循环
            break
        time.sleep(1)


if __name__ == "__main__":
    start_trace('183.232.231.174', 30)
