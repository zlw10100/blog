# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'


"""一个简单的实现职责链模式的程序
此程序模拟向公司领导申请加薪，不同的加薪程度需要不同级别的领导审批。
"""


from src.managers import (
    CompanyManager,
    DepartManager,
    ProjectManager,
)

from src.events import SalaryIncreaseEvent


if __name__ == '__main__':
    # 职责对象
    boss = CompanyManager()
    depart_manager = DepartManager()
    project_manager = ProjectManager()

    # 设定职责链条顺序
    depart_manager.set_boss(boss)
    project_manager.set_boss(depart_manager)

    # 事件对象
    apply_1500 = SalaryIncreaseEvent(money=1500)
    apply_3500 = SalaryIncreaseEvent(money=3500)
    apply_8500 = SalaryIncreaseEvent(money=8500)
    apply_13500 = SalaryIncreaseEvent(money=13500)

    # 调用对象处理申请(任选其一，根据金额不同，权签人也不同)
    # project_manager.handle(apply_1500)
    # project_manager.handle(apply_3500)
    project_manager.handle(apply_8500)
    # project_manager.handle(apply_13500)
