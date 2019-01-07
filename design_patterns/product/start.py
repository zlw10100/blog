# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

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











