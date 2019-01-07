# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


from abc import ABCMeta, abstractmethod

class AbstractSubject(object, metaclass=ABCMeta):
    def __init__(self, event_delegate):
        self.state_change = False
        # 指定事件委托对象
        self.event_delegate = event_delegate

    @abstractmethod
    def notify(self):
        pass


# 主题：歌曲更新
class SongUpdateSubject(AbstractSubject):
    def notify(self):
        if self.state_change is True:
            self.event_delegate.update(self)

# 主题：站点维护
class SiteMaintainSubject(AbstractSubject):
    pass
    







