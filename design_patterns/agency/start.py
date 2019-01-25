# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现中介模式的程序
此程序模拟了联合国和国家的角色，
联合国作为中介负责传递消息。
"""


from src.agencys import UN
from src.customers import Country


if __name__ == '__main__':
    # 创建中介对象
    un = UN()

    # 创建客户对象，并加入中介的客户清单中
    china = Country('中国')
    un.add(china)

    america = Country('美国')
    un.add(america)

    england = Country('英国')
    un.add(england)

    # 中介向所有客户发送消息
    un.publish('世界杯开始啦!')

    # 某一个客户向另一个客户发消息，由中介转发
    china.send(america, msg='呵呵')
