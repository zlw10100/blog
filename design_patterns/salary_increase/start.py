# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 'author':'zlw'



from src.managers import (
    CompanyManager,
    DepartManager,
    ProjectManager,
)

from src.events import SalaryIncreaseEvent


if __name__ == '__main__':
    # 领导对象
    boss = CompanyManager()
    depart_manager = DepartManager()
    project_manager = ProjectManager()

    # 设定职责链条顺序
    depart_manager.set_boss(boss)
    project_manager.set_boss(depart_manager)

    # 事件对象
    application_1500 = SalaryIncreaseEvent(money=1500)
    application_3500 = SalaryIncreaseEvent(money=3500)
    application_8500 = SalaryIncreaseEvent(money=8500)
    application_13500 = SalaryIncreaseEvent(money=13500)

    # 调用对象处理申请
    # project_manager.handle(application_1500)
    # project_manager.handle(application_3500)
    project_manager.handle(application_8500)
    # project_manager.handle(application_13500)

































