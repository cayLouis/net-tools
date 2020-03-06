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
import os
import time


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


def deal_list(lis, fun):
    for i in lis:
        fun(i)


def trans_file(ip, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(3)
    print("服务器开启成功 \n 等待连接...")
    while True:
        conn, addr = sock.accept()
        print("来自%s的连接" % str(addr))
        mess = conn.recv(1024).decode("utf-8")
        # 显示当前目录中的文件
        if mess == "1":
            deal_list(os.listdir(os.getcwd()), lambda x: conn.sendall(x.encode('utf-8') + b'\n'))
        elif mess == "0":
            conn.close()
        else:
            print(12)
            if os.path.exists(mess):
                cur_size = 0
                size = os.path.getsize(mess)
                conn.sendall(str(size).encode("utf-8"))
                print("heko")
                time.sleep(0.5)
                with open(mess, "rb") as f:
                    while cur_size != size:
                        print("start...")
                        data = f.read(1024)
                        conn.sendall(data)
                        cur_size += len(data)
                        print('\r' + "[发送进度]%s%.02f%%" % (">"*int(cur_size/size)*50, cur_size/size*100))
            else:
                conn.sendall("文件不存在".encode("utf-8"))


if __name__ == "__main__":
    trans_file("127.0.0.1", 4321)




