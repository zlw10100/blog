# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""TCP服务器模块
此模块定义了以tcp socket为基础的服务器的请求处理业务逻辑。
"""


from src.templates import TCPServerTemplate


class TCPServer(TCPServerTemplate):
    def process_request(self, request):
        request = build(request)
        response = self.handle(request)
        return response

    def build(self, request):
        # 构造请求对象
        pass

    def handle(self, request):
        # 处理请求对象并返回响应数据
        pass
