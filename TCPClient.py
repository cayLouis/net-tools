#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   TCPClient.py    
@Contact :   815569735@qq.com
@License :   (C)Copyright 2017-2018, Louis-NLPR-CASIA
@Modify Time :    2020/2/29 0029 17:12
@Author :    louis
@Version :    1.0
@Description :    此文件用于创建一个TCP客户端
"""

# import lib
from socket import *
import tinyTools


def connect_server(ip, port):
    sock_cli = socket(AF_INET, SOCK_STREAM)
    sock_cli.connect((ip, port))
    while True:
        message = input("Input what you want to send:")
        # 空字符串和None是两种不同的类型，'' != None
        if message == '':
            break
        data = message.encode("utf-8")
        # 这里有一个错误，不是因为input函数不能什么都不输入，是因为socket不能发送空字符串
        sock_cli.send(data)
        recv_data = sock_cli.recv(1024)
        print("Client Received:" + recv_data.decode("utf-8"))
    sock_cli.close()


if __name__ == "__main__":
    connect_server(tinyTools.get_ip(), 6666)