# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


class BaseServer(object):
    def get_file(self, filename):
        print('下载', filename)

class FTPServer(BaseServer):
    def leave_msg(self, msg):
        print('用户留言:', msg)

# 代理应该与实际被调用者是同一类对象（至少要表现的像同一类对象）
class Proxy(BaseServer):
    def __init__(self):
        # 指向被代理对象
        self.instance = FTPServer()
        
    # 要构造被代理的方法，实际业务处理还是要让被调用者处理，代理只实现额外的逻辑控制
    def get_file(self, filename):
        print('检查调用者的权限')
        return self.instance.get_file(filename)

    def leave_msg(self, msg):
        print('记录日志')
        return self.instance.leave_msg(msg)


if __name__ == '__main__':
    ftp = Proxy()

    filename = 'robots.txt'
    ftp.get_file(filename)

    msg = '文章质量不错!'
    ftp.leave_msg(msg)








