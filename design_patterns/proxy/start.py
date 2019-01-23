# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现代理模式的程序
用一个代理类代表真实的FTP类，用户可以通过调用代理类提供的接口得到FTP的数据。
"""


class BaseServer(object):
    def get_file(self, filename):
        print('下载:', filename)


class FTPServer(BaseServer):
    def leave_msg(self, msg):
        print('留言:', msg)


# 代理应该与实际被调用者是同一类对象（至少要表现的像同一类对象）
class Proxy(BaseServer):
    def __init__(self):
        self.instance = FTPServer()  # 指向被代理对象

    # 要构造被代理的方法，实际业务处理还是要让被调用者处理，代理只实现额外的逻辑控制
    def get_file(self, filename):
        print('检查调用者的权限')
        return self.instance.get_file(filename)

    def leave_msg(self, msg):
        print('记录日志')
        return self.instance.leave_msg(msg)


if __name__ == '__main__':
    ftp_proxy = Proxy()

    filename = 'robots.txt'
    ftp_proxy.get_file(filename)
    # 检查调用者的权限
    # 下载: robots.txt

    msg = '文章质量不错!'
    ftp_proxy.leave_msg(msg)
    # 记录日志
    # 留言: 文章质量不错!
