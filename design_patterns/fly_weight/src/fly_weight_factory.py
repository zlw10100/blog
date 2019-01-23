# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""享元工厂模块"""


from src.websites import site_map


class WebFactory(object):
    def get_site(self, name):
        if name in site_map:
            return site_map[name]  # 共享同一个享元对象实例
