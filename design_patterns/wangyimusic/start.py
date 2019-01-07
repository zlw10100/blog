# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'




from src.subjects import (
    SongUpdateSubject,
    SiteMaintainSubject
)
from src.delegate import EventDelegate
from src.observers import (
    MusicAPP,
    QQEmail,
    MusicCDN,
)



if __name__ == '__main__':
    # 实例化主题
    song_update_subject = SongUpdateSubject()
    # 实例化观察者
    app = MusicAPP()
    email = QQEmail()
    cdn = MusicCDN()

    # 实例化事件委托并注册观察者
    eve_delegate = EventDelegate()
    eve_delegate.register(song_update_subject, app.download_song)
    eve_delegate.register(song_update_subject, email.notice_info)
    eve_delegate.register(song_update_subject, cdn.upload_song)

    # 发生歌曲更新
    song_update_subject.state_change = True
    # 通知所有订阅此主题的用户
    song_update_subject.notify()










