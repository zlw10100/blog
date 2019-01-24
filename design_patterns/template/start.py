# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.tcpserver import TCPServer


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    
    server = TCPServer(ip, port)
    server.run()
