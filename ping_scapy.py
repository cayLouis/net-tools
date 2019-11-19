from scapy.all import *
import time
import re
import sys
import random


def ping_one_raw(pdst, id, seq, ttl=64):
    send_time = time.time()
    #按指定格式转化时间，网络字节序为大端，较低的有效字节存放在较高的储存器地址中
    send_time_bin = struct.pack(">d",send_time)

    ping_one_response = sr1(IP(dst=pdst, ttl=ttl)/ICMP(id=id, seq=seq)/send_time_bin, timeout=2, verbose=False)
    try:
        if ping_one_response.getlayer(ICMP).type == 0 and ping_one_response.getlayer(ICMP).code == 0 and ping_one_response.getlayer(ICMP).id == id:
            reply_soure_ip = ping_one_response.getlayer(IP).src
            
            reply_seq = ping_one_response.getlayer(ICMP).seq
            reply_ttl = ping_one_response.getlayer(IP).ttl
            reply_data_length = len(ping_one_response.getlayer(Raw).load) + 8
            reply_data = ping_one_response.getlayer(Raw).load
            receive_time = time.time()
            print(2)
            echo_send_time = struct.unpack(">d", reply_data)

            time_pass = (receive_time-echo_send_time[0])*1000

            return reply_data_length, reply_soure_ip, reply_seq, reply_ttl, time_pass
    except Exception as e:
        if re.match(".*NoneType.*", str(e)):
            return None

if __name__ == "__main__":
    if(len(sys.argv)==2):
        pdst = sys.argv[1]
        id = os.getpid()
        seq = random.randint(0,100)
        response=ping_one_raw(pdst, id, seq)
        if response:
            print("{0} bytes from {1}: icmp_seq={2} ttl={3} time={4:.3f} ms".format(response[0],response[1],response[2],response[3],response[4]))
        else:
            print("无响应")
    else:
        print("输入的参数错误")
