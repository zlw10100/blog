# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from src.computers import (
    DesktopComputer,
    LaptopComputer,
)

from src.softwares import (
    ChatSoft,
    VideoSoft,
    MusicSoft,
)


if __name__ == '__main__':
    chat = ChatSoft('qq')
    video = ChatSoft('腾讯视频')
    music = ChatSoft('网易云音乐')

    # 台式电脑硬件实例化
    desk_com = DesktopComputer()
    # 桥接(组合)软件
    desk_com.set_software(chat)
    desk_com.set_software(video)
    desk_com.set_software(music)
    desk_com.show_softwares()

    # 笔记本电脑硬件实例化
    laptop_com = LaptopComputer()
    # 桥接(组合)软件
    laptop_com.set_software(chat)
    laptop_com.set_software(video)
    laptop_com.set_software(music)
    laptop_com.show_softwares()







