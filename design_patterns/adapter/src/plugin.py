# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""第三方插件模块
此插件可以为指定的手机号发送短信。
"""


# 模拟第三方短信插件的接口
def send_message(phone, content, appid, appkey):
    print('调用者的账户信息是:', appid, appkey)
    print('验证调用者账户信息')
    print(f'执行短信发送，为{phone}发送内容{content}')
