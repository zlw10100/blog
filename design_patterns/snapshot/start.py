# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/1/25


"""一个简单的实现快照模式的程序
此程序模拟一个游戏角色的快照保存流程。
"""


from src.originators import GameOriginator
from src.snapshots import GameSnapshot
from src.managers import GameManager


if __name__ == '__main__':
    # 实例化游戏快照管理者对象
    game_manager = GameManager()

    # 实例化游戏角色，小鱼人
    fizz = GameOriginator(100, 30000)
    print(fizz.info)
    # (100, 30000)

    # 在打boss前保存快照
    snapshot = fizz.save_state(GameSnapshot)
    # 设置快照的索引
    index='boss-0125',
    # 保存快照
    game_manager.save(index, snapshot)

    # 开始打boss
    fizz.attack_boss()
    print(fizz.info)
    # (77, 25000)

    # 不满意，加载上一次游戏状态
    # 根据索引提取快照
    snapshot = game_manager.extract(index)
    fizz.set_state(snapshot)
    print(fizz.info)
    # (100, 30000)
