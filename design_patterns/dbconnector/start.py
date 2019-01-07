# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



from src.db_facade import DBFacade


if __name__ == '__main__':
    data = 'some data'
    
    db = DBFacade('redis')
    
    db.save(data)
    








