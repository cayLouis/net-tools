from . import tinyTools
from scapy.all import *
import time
import multiprocessing


# 用于发送DHCP协议中的Discover报文
def DHCP_Discover(ifname, MAC, wait_time = 1):
    """
    :param ifname:传递接口名称
    :param MAC:所用接口的MAC地址
    :param wait_time:等待时间
    :return:None
    """
    if wait_time !=0:
        time.sleep(wait_time)
    Bytes_MAC = tinyTools.change_mac_to_bytes(MAC)
    # chaddr全拼为client hardware address总共为16个字节，MAC占6字节
    # discover包中的选项字段只需声明消息字段即可
    discover = (Ether(dst="ff:ff:ff:ff:ff:ff", src=MAC, type=0x0800)
        / IP(src="0.0.0.0", dst="255.255.255.255")
        / UDP(dport=67, sport=68)
        / BOOTP(op=1, chaddr=Bytes_MAC + b"\x00"*10)
        / DHCP(options=[('message-type','discover'), 'end']))
    sendp(discover, iface=ifname, verbose=False)


# 用于发送DHCP协议中的Request报文
def DHCP_Request(ifname, options, wait_time=1):
    """
    :param options: 从offer报文中得到的信息字典
    :param wait_time:延迟发送的秒数
    :return: None
    """
    # BOOTP层中siaddr为server ip address
    # DHCP层中client_id是客户端的MAC地址，01前缀表示是以太网类型
    request = Ether(dst="ff:ff:ff:ff:ff:ff", src=options['MAC'], type=0x0800)\
        /IP(src="0.0.0.0", dst="255.255.255.255")\
        /UDP(dport=67,sport=68)\
        /BOOTP(op=1, chaddr=options['client_id'] + b'\x00'*10, siaddr=options['Server_IP'],)\
        /DHCP(options=[('message-type', 'request'),
                       ('server_id', options['Server_IP']),
                       ('requested_addr', options['requested_addr']),
                       ('client_id', b'\x01' + options['client_id']), ('end')])
    if wait_time != 0:
        time.sleep(wait_time)
    sendp(request, iface=ifname, verbose=False)


def DHCP_Monitor_Control(pkt):
    try:
        if pkt.getlayer(DHCP).fields['options'][0][1] == 1:
            print("发现DHCP Discover包，MAC地址为：", end='')
            MAC_Bytes = pkt.getlayer(BOOTP).fields['chaddr']
            MAC_chddr = tinyTools.change_bytes_to_mac(MAC_Bytes)
            MAC_Addr = MAC_chddr[:17]
            print(MAC_Addr)
            print("Discover包中发现如下Options：")
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == "end":
                    break
                # 15表示占位符宽度，-表示向左对齐
                print("%-15s ==> %s" %(str(option[0]), str(option[1])))
        elif pkt.getlayer(DHCP).fields["options"][0][1] == 2:
            options = {}
            MAC_Bytes = pkt.getlayer(BOOTP).fields['chaddr']
            MAC_chddr = tinyTools.change_bytes_to_mac(MAC_Bytes)
            MAC_Addr = MAC_chddr[:17]
            options['MAC'] = MAC_Addr
            options['client_id'] = tinyTools.change_mac_to_bytes(MAC_Addr)
            print("发现DHCP OFFER包，请求者得到的IP为：" + pkt.getlayer(BOOTP).fields['yiaddr'])
            print("OFFER包中发现如下options：")
            for option in pkt.getlayer(DHCP).fields["options"]:
                if option == "end":
                    break
                print("%-15s ==> %s" %(str(option[0]), str(option[1])))
            options['requested_addr'] = pkt.getlayer(BOOTP).fields['yiaddr']
            for i in pkt.getlayer(DHCP).fields['options']:
                if i[0] == 'server_id':
                    options["Server_IP"] = i[1]
            Send_Request = multiprocessing.Process(target=DHCP_Request, args=(Global_IF, options))
            Send_Request.start()
        elif pkt.getlayer(DHCP).fields['options'][0][1] == 3:
            print("发现DHCP Request包，请求的IP为" + pkt.getlayer(BOOTP).fields['siaddr'])
            print("Request包中发现如下options：")
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    break
                print("%-15s ==> %s" %(str(option[0]), str(option[1])))
        elif pkt.getlayer(DHCP).fields['options'][0][1] == 5:
            print("发现DHCP ACK包，确认的IP为：" + pkt.getlayer(BOOTP).fields[''])
            print("ACK包中发现如下options：")
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == "end":
                    break
                print('%-15s ==> %s' %(str(option[0]), str(option[1])))
    except Exception as e:
        print(e)
        pass


def DHCP_Full(ifname, MAC, timeout=10):
    # global用于声明全局变量
    global Global_IF
    Global_IF = ifname
    # Process()方法用于产生一个新的进程来发送discover包
    Send_Discover = multiprocessing.Process(target=DHCP_Discover, args=(Global_IF, MAC))
    Send_Discover.start()
    # filter参数和tcpdump的选项格式相似，store参数用来表示是否将包存储在本地
    # prn参数传递函数名，表示用这个函数来处理抓到的包！！
    sniff(prn=DHCP_Monitor_Control, filter="port 68 and port 67", store=0, iface=Global_IF, timeout=timeout)


if __name__ == "__main__":
    DHCP_Full("wlan0", tinyTools.get_mac())






