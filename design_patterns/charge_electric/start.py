# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



class Computer(object):
    def electric_input(self, v):
        assert v <= 220, '电压太大'
        print('电脑充上电')



class Car(object):
    def electric_output(self):
        print('汽车输出电')
        return 500


class Adapter(Car):
    def __init__(self):
        self.car = Car()

    # 适配器获取真实车辆的电量，并做兼容性转换
    def electric_output(self):
        v = self.car.electric_output()
        if v > 220:
            v = 220
        return v


if __name__ == '__main__':
    com = Computer()
    # 实例化一个装配了适配器的车对象
    adapter_car = Adapter()

    # 电脑使用装配了适配器的车进行充电
    com.electric_input(adapter_car.electric_output())

    # com.electric_input(car.electric_output())













