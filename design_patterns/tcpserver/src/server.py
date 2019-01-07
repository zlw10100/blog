# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.baseserver import BaseServer


class TCPServer(BaseServer):
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









