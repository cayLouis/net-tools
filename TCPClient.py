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


def rece_file(ip, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip, port))
    while True:
        print('''
        1.显示当前目录存在的文件
        0.退出
        ---------------------
        输入文件名进行下载''')
        mess = input("输入你想进行的操作：")
        mess_byte = mess.encode('utf-8')
        if mess == '':
            print("选项错误！！！")
        elif mess == '1':
            sock.send(mess_byte)
            data = sock.recv(1024)
            print(data.decode('utf-8'))
        elif mess == '0':
            sock.send(mess_byte)
            break
        else:
            sock.send(mess_byte)
            with open(mess, "wb") as f:
                while True:
                    data = sock.recv(1024)
                    if not len(data):
                        break
                    f.write(data)
    sock.close()


if __name__ == "__main__":
    rece_file("127.0.0.1", 4321)
