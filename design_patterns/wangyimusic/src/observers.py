# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod

class AbstractObserver(object, metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass


class MusicAPP(AbstractObserver):
    def download_song(self):
        print('网易云音乐app收到通知，准备下载歌曲')
    

class QQEmail(AbstractObserver):
    def notice_info(self):
        print('qq邮箱收到通知，准备发邮件告知用户')


class MusicCDN(AbstractObserver):
    def upload_song(self):
        print('音乐cdn服务器收到通知，准备上线新歌曲')






