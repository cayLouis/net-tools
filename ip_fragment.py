from scapy.all import *

dst = '192.168.1.1'


# 手动进行IP分片
def get_result():
    # 这里的flags参数即为IP协议中的MF位
    # IP其他分片中不包含UDP头部，所以需要指明协议proto
    # 标准的ICMP头部为8个字节
    # frag表示偏移量，以8个字节为单位
    send(IP(id=1, flags=1, frag=0, dst=dst)/ICMP(chksum=0x192c)/b'welcome to louis........')
    send(IP(id=1, flags=1, frag=4, dst=dst, proto=1)/b'welcome to louis........welcomee')
    send(IP(id=1, flags=0, frag=8, dst=dst, proto=1)/b'the ending')
# 若要自动进行IP分片，则只需让发送的包的长度大于MTU即可
get_result()