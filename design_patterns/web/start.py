# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.web_factory import WebFactory


if __name__ == '__main__':
    factory = WebFactory()

    name = 'news'
    site = factory.get_site(name)
    site.run(username='zlw')

    name = 'news'
    site = factory.get_site(name)
    site.run(username='kaka')











