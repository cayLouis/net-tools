from scapy.all import *

"""
该程序通过DNS协议获取网站对应的ip地址
"""


def dns_query(dns_name):
    # 114.114.114.114为国内移动、联通、电信通用的DNS服务器
    # id为标识字段，一般要求DNS请求与回应的标识字段相同
    # qr为查询响应标志，0表示查询，1表示回应
    # opcode为操作码，0表示标准查询
    # rd表示期望递归
    # qd表示要查询的域名
    dns_result = sr1(IP(dst="114.114.114.114") / UDP() / DNS(id=168, qr=0, opcode=0, rd=1, qd=DNSQR(qname=dns_name)),
                     verbose=False)
    layer = 0
    while True:
        try:
            if dns_result.getlayer(DNS).fields["an"][layer].fields['type'] == 1:
                dns_result_ip = dns_result.getlayer(DNS).fields['an'][layer].fields['rdata']
                print(dns_result_ip)
            layer += 1
        except:
            break

def dns_query_reserve(dns_name):
    dns_result = sr1(IP(dst="114.114.114.114") / UDP() / DNS(id=169, qr=0, opcode=1, rd=0, qd=DNSQR(qname=dns_name)), verbose=False)
    layer = 0
    while True:
        try:
            print(dns_result.getlayer(DNS))
            if dns_result.getlayer(DNS).fields["an"][layer].fields['type'] == 1:
                dns_result_ip = dns_result.getlayer(DNS).fields['an'][layer].fields['rdata']
                print(dns_result_ip)
            layer += 1
        except:
            break


if __name__ == "__main__":
    # dns_query("www.baidu.com")
    dns_query_reserve("14.215.177.38")
