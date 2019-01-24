# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""底层服务器模块
此模块定义了TCP socket形式的服务器的请求接收和发送过程，
但是请求的业务处理过程只定义了函数签名，并未实现，实现交由子类处理。
"""


import socket


class TCPServerTemplate(object):
    RECV_BUFFER = 4096
    SEND_BUFFER = 4096

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.listen = 5
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def prepare(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(self.listen)
        print('socket准备就绪，监听中...')

    def process_request(self, request):
        # 其他步骤都是固定的编写完毕，需要子类自行实现此步骤逻辑
        raise NotImplementedError(f'你必须实现此方法以完成请求处理逻辑')

    def loop(self):
        while True:
            conn, addr = self.socket.accept()
            while True:
                request = conn.recv(self.RECV_BUFFER)
                response = self.process_request(request)
                conn.send(response)

    def run(self):
        self.prepare()
        self.loop()
