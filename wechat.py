#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   wechat.py.py    
@Contact :   815569735@qq.com
@License :   (C)Copyright 2017-2018, Louis-NLPR-CASIA
@Modify Time :    2020/3/6 0006 10:06
@Author :    louis
@Version :    1.0
@Description :    None
"""

# import lib
import falcon
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException


class Connect(Object):

    def on_get(self, req, resp):
        query_string = req.query_string
        query_list = query_string.split("&")
        b = {}
        for i in query_list:
            b[i.split("=")[0]] = i.split("=")[1]

        try:
            check_signature(token="0121709361809", signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200


if __name__ == "__main__":
    app = falcon.API()
    connect = Connect()
    app.add_route('/connect', connect)
