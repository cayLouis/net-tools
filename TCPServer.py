#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   TCPServer.py    
@Contact :   815569735@qq.com
@License :   (C)Copyright 2017-2018, Louis-NLPR-CASIA
@Modify Time :    2020/2/29 0029 17:01
@Author :    louis
@Version :    1.0
@Description :    此文件用socket模块创建一个TCP回显服务器
"""

# import lib
from socket import *
import tinyTools


def creat_server(port):
    # 获取本机的IP地址
    myip = tinyTools.get_ip()
    myport = port
    # 创建一个socket对象
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.bind((myip, myport))
    sockobj.listen(5)
    while True:
        connection, address = sockobj.accept()
        print("Server connected by ", address)
        # 数据在网络中是以字节流的形式进行传输的
        while True:
            data = connection.recv(1024)
            print("receive:" + data.decode('utf-8'))
            if not data:break
            connection.send(b'Echo==> ' + data)
        connection.close()


def trans_file():
    myip = tinyTools.get_ip
if __name__ == "__main__":
    creat_server(6666)




