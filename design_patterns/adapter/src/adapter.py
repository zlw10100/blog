# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.plugin import send_message


def send_sms(content, to, account):
    # 此接口接收项目的调用，处理输入参数后再次调用第三方插件接口
    phone = to.get('phone')
    appid = account.get('appid')
    appkey = account.get('appkey')
    
    send_message(phone, content, appid, appkey)
