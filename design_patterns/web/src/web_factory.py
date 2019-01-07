# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.websites import site_map


class WebFactory(object):
    def get_site(self, name):
        if name in site_map:
            return site_map[name]












