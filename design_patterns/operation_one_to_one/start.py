# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.factorys import (
    AddFactory,
    DivisionFactory,
)


if __name__ == '__main__':
    a = 23
    b = 44
    add_factory = AddFactory()
    add = add_factory.create_operate()
    print(add.handle(a, b))

    c = 100
    d = 10
    division_factory = DivisionFactory()
    division = division_factory.create_operate()
    print(division.handle(c, d))










