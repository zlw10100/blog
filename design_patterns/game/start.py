# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

from src.player import Player
from src.admin import RecordAdmin


if __name__ == '__main__':
    quanhuang = Player('拳皇', 77, 49, 110)
    record_admin = RecordAdmin()

    print('打boss前')
    quanhuang.show_state()
    record = quanhuang.save_state()
    record_admin.save(record)

    print('打boss')
    quanhuang.fight_boss()
    quanhuang.show_state()

    # 不行，要恢复游戏记录重新打boss
    print('恢复记录')
    history_record = record_admin.extract()
    quanhuang.set_state(history_record)
    quanhuang.show_state()













