# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.agencys import UN
from src.customers import Country


if __name__ == '__main__':
    # 创建中介对象
    un = UN()

    # 创建客户对象，并加入中介的客户清单中
    china = Country('中国')
    un.add_customer(china)

    america = Country('美国')
    un.add_customer(america)

    england = Country('英国')
    un.add_customer(england)

    # 中介向所有客户发送消息
    un.send_all('世界杯开始啦!')





























