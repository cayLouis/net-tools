from scapy.all import *
"""
该程序通过DNS协议获取网站对应的ip地址
"""

def dns_query(dns_name):
    dns_result = sr1(IP(dst="114.114.114.114")/UDP()/DNS(id=168,qr=0,opcode=0,rd=1,qd=DNSQR(qname=dns_name)),
                     verbose=False)
    layer = 0
    while True:
        try:
            if dns_result.getlayer(DNS).fields["an"][layer].fields['type'] == 1:
                dns_result_ip = dns_result.getlayer(DNS).fields['an'][layer].fields['rdata']
                print(dns_result_ip)
            layer+=1
        except:
            break

if __name__ == "__main__":
    dns_query("")
