# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


# 记录管理员
class RecordAdmin(object):
    def __init__(self):
        self.record_list = list()

    def save(self, record):
        self.record_list.append(record)
    
    def extract(self, record_id=-1):
        return self.record_list.pop(record_id)
        
        










