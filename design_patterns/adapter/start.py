# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的第三方插件适配器程序
第三方插件的接口设计与项目的接口设计并不兼容，
此时可以为插件编写一个适配器以兼容项目的接口。
"""


from src.adapter import send_sms


if __name__ == '__main__':
    # 用户对象
    user = {
        'phone': '18888888888',
        'name': 'xxx',
        'age': 27,
    }

    # 第三方短信平台账户对象
    plugin_account = {
        'appid': 'asdjfklsdajflsad',
        'appkey': 'adsfhptiureiotrjenmxcvx',
    }

    # 希望直接通过以上两个对象的数据调用第三方短信发送接口
    send_sms(content='验证码是:7878', to=user, account=plugin_account)
    # 调用者的账户信息是: asdjfklsdajflsad
    # adsfhptiureiotrjenmxcvx
    # 验证调用者账户信息
    # 执行短信发送，为18888888888发送内容验证码是: 7878
