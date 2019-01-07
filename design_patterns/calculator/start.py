# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



from src.cal.cal import Cal
from src.view.view import View

def run():
    v = View()
    a, b, o = v.view()

    c = Cal()
    c.cal(a, b, o)


if __name__ == '__main__':
    run()















