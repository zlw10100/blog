# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的构造建筑物的程序。
有两个建筑物：博物馆和歌剧院。
两个建筑物的构造过程相同，但是构造细节不同，使用建造者模式详细定义和管理建造过程。
"""


from src.commander import Commander
from src.builders import (
    MuseumBuilder,
    OperaBuilder,
)


if __name__ == '__main__':
    # 实例化指挥官
    commander = Commander()
    # 用户选择某一个构造者
    museum_builder = MuseumBuilder()

    # 告诉指挥官，驱动建造者开始构造
    commander.drive_construct(museum_builder)

    # 从构造者获取产品
    museum = museum_builder.get_result()
    museum.show()
    # 部件: 博物馆的基座
    # 部件: 博物馆的墙面
