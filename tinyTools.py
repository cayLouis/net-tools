import uuid
import socket
import os
import re
import sys
"""
此小工具用于获取本机的Mac地址和IP地址
"""


def get_mac():
    id = check_platform()
    if id == 1:
        return get_mac_linux()
    if id == 2:
        return get_mac_win()
    if id == 0:
        try:
            raise Exception()
        except Exception as e:
            print("获取mac地址错误")


def get_mac_win():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


def get_mac_linux():
    result = os.popen("ifconfig")
    regex = re.compile('ether\s(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})')
    match_result = regex.findall(result.read())
    return match_result[1]


def get_ip():
    # getfqdn()用于从名字得到完整的域名,当然，直接用gethostname()也可
    hostname = socket.getfqdn(socket.gethostname())
    # ip = socket.gethostbyname(hostname)
    ip = socket.gethostbyname(socket.gethostname())
    return ip


def change_mac_to_bytes(MAC) -> bytes:
    mac_list = MAC.split(":")
    # fromhex()函数将16进制字符串转化为字节流
    # bin_mac = [bytes.fromhex(x).decode('utf-8') for x in mac_list]
    bin_mac = "".join(mac_list)
    bin_mac_str =  bytes.fromhex(bin_mac)
    return bin_mac_str


def change_bytes_to_mac(mac_byte) -> str:
    # bytes.hex()用于将字节流转化为16进制字符串
    mac_str = mac_byte.hex()
    mac_list = [mac_str[i:i+2] for i in range(0,len(mac_str),2)]
    mac = ":".join(mac_list)
    return mac


def check_platform():
    plat = sys.platform
    regex_linux = re.compile("linux")
    regex_win = re.compile("win")
    result_l = regex_linux.search(plat)
    result_w = regex_win.search(plat)
    if result_l is not None:
        return 1
    elif result_w is not None:
        return 2
    else:
        return 0


if __name__ == "__main__":
    print(get_mac())

