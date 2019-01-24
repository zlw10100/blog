# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现模板方法模式的程序
此程序实现一个非常简单的tcp socket服务器，
在模板中已经完成服务器的固定实现，但是业务逻辑的处理交由子类实现。
"""


from src.tcpserver import TCPServer


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    
    server = TCPServer(ip, port)
    server.run()
