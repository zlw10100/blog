# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'

from copy import copy


# 原型类，提供clone克隆接口
class Prototype(object):
    def clone(self):
        raise NotImplementedError('方法必须被实现')


class Profile(object):
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def clone(self):
        return copy(self)

    def show(self):
        print('个人简历信息:')
        print(str(self.__dict__))


if __name__ == '__main__':
    profile = Profile('zlw', 27, '男')

    # 要20份个人档案
    profile_list = list()
    for i in range(20):
        # 使用克隆（复制）来实现20份档案，而不是实例化20次
        profile_list.append(profile.clone())

    print(profile_list)


