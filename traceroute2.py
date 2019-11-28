from scapy.all import *
import time


def response(ip, dport, ttl):
    send_time = time.time()
    resp = sr1(IP(dst=ip, ttl=ttl) / UDP(dport=dport), verbose=False, timeout=1)
    type_no = resp.getlayer(ICMP).type
    code_no = resp.getlayer(ICMP).code
    try:
        if type_no == 11 and code_no == 0:
            psrc = sr1.getlayer(IP).src
            recv_time = time.time()
            time_passed = (recv_time - send_time) * 1000
            return 1, psrc, time_passed
        elif type_no == 3 and code_no == 3:
            psrc = sr1.getlayer(IP).src
            recv_time = time.time()
            time_passed = (recv_time - send_time) * 1000
            return 2, psrc, time_passed
    except Exception as e:
        if re.match('.*NoneType.*', str(e)):
            return None


def start_trace(dst, hops):
    dport = 24536
    hop = 0
    while hop < hops:
        dport = dport + hop
        hop+=1
        result = response(dst, dport, hop)
        if result is None:
            print(str(hop) + ' *', flush=True)
        elif result[0] == 1:
            time_to_pass = '%4.2f' %result[2]
            print(str(hop) + ' ' + str(result[1]) + ' ' + time_to_pass)
        elif result[0] == 2:
            time_to_pass = '%4.2f' %result[2]
            print(str(hop) + ' ' + str(result[1]) + ' ' + time_to_pass)
            break
        time.sleep(1)


if __name__ == "__main__":
    start_trace('183.232.231.174', 30)


