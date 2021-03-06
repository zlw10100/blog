# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2019/2/23


"""
表达式求值
先对所有子表达式递归求值（基础表达式就是自求值）
然后对复合表达式求值
求值过程是一棵树，递归求值，叶子节点是基础表达式


指代的能力
用一个符号代表一个/一组/一类值。
程序中的实现是：变量赋值。
值有类型、范围的区别。
符号如果严格要求与值类型相同就是静态类型，
否则就是动态类型，即支持泛型。
a = 3，是一种抽象到具体的行为。
程序中的赋值，是将值的地址赋给变量，变量保存值的地址。
赋值导致了上下文环境的产生。


为什么将值区分为数据和函数？是否应该区分？
pass

赋值记录表
赋值后产生变量->值的关系记录表，就是上下文环境
当需要查找某一个变量所指代的值时，从此表中搜索
程序最初就是main函数，所以是函数栈的最底层，
此时环境是全局环境

局部环境
函数被调用的时候，会在当前函数栈的顶部再入栈一个函数栈，
新函数被运行，程序视角在新函数中。
新函数自己的栈帧中开辟一个局部的环境，
可以直接使用环境中已存在的数据（比如由调用者传递进来的）
也可以自己新增数据，
也可以寻找环境中没有的数据，那么就要向全局方向搜索。
尽量少的搜索全局。
执行完毕后，将局部环境中的某些数据地址返回给调用者。
新函数返回。
调用者拿到结果数据的地址并执行赋值，新函数栈帧被销毁，
程序视角回到调用者，调用者的局部环境中新增结果数据。

python的模块文件也是局部变量（称为模块文件的全局环境）
当前文件运行时数据都在本模块中寻找，找不到才找内置，
模块文件之间不会搜索。
所以只有内置环境才是真正的全局环境，模块搜索不到时，
就会搜索内置环境，内置环境应该存放所有模块都会使用
的常用对象，如print。

所有python模块文件都是作为局部环境，找不到的话就
找内置环境，不会在模块文件之间搜索的。

"""




































































































