[TOC]

**（为了方便和美观，省略了各内置方法前后的__双下划线）**

---


### 1、new、init

`__new__`方法是真正的类构造方法，用于产生实例化对象（空属性）。重写`__new__`方法可以控制对象的产生过程。
`__init__`方法是初始化方法，负责对实例化对象进行属性值初始化，此方法必须返回None，`__new__`方法必须返回一个对象。重写`__init__`方法可以控制对象的初始化过程。
```python
# 使用new来处理单例模式

class Student:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def sleep(self):
        print('sleeping...')

stu1 = Student()
stu2 = Student()

print(id(stu1), id(stu2))  # 两者输出相同
print(stu1 is stu2)  # True
```
个人感觉，`__new__`一般很少用于普通的业务场景，更多的用于元类之中，因为可以更底层的处理对象的产生过程。而`__init__`的使用场景更多。

### 2、str、repr
两者的目的都是为了显式的显示对象的一些必要信息，方便查看和调试。`__str__`被`print`默认调用，`__repr__`被控制台输出时默认调用。即，使用`__str__`控制用户展示，使用`__repr__`控制调试展示。
```python
# 默认所有类继承object类，object类应该有一个默认的str和repr方法，打印的是对象的来源以及对应的内存地址

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

stu = Student('zlw', 26)
print(stu)  # <__main__.Student object at 0x0000016ED4BABA90>

```
```python
# 自定义str来控制print的显示内容，str函数必须return一个字符串对象
# 使用repr = str来偷懒控制台和print的显示一致

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'{self.__class__}, {self.name}, {self.age}'

    __repr__ = __str__

stu = Student('zlw', 26)
print(stu)  # <class '__main__.Student'>, zlw, 26


```

### 3、call
`__call__`方法提供给对象可以被执行的能力，就像函数那样，而本质上，函数就是对象，函数就是一个拥有`__call__`方法的对象。拥有`__call__`方法的对象，使用`callable`可以得到`True`的结果，可以使用`（）`执行，执行时，可以传入参数，也可以返回值。所以我们可以使用`__call__`方法来实现实例化对象作为装饰器：
```python

# 检查一个函数的输入参数个数, 如果调用此函数时提供的参数个数不符合预定义，则无法调用。

# 单纯函数版本装饰器
def args_num_require(require_num):
    def outer(func):
        def inner(*args, **kw):
            if len(args) != require_num:
                print('函数参数个数不符合预定义，无法执行函数')
                return None

            return func(*args, **kw)
        return inner
    return outer

@args_num_require(2)
def show(*args):
    print('show函数成功执行!')

show(1)  # 函数参数个数不符合预定义，无法执行函数
show(1,2) # show函数成功执行!
show(1,2,3)  # 函数参数个数不符合预定义，无法执行函数
```

```python

# 检查一个函数的输入参数个数,
# 如果调用此函数时提供的参数个数不符合预定义，则无法调用。

# 实例对象版本装饰器
class Checker:
    def __init__(self, require_num):
        self.require_num = require_num

    def __call__(self, func):
        self.func = func

        def inner(*args, **kw):
            if len(args) != self.require_num:
                print('函数参数个数不符合预定义，无法执行函数')
                return None

            return self.func(*args, **kw)
        return inner

@Checker(2)
def show(*args):
    print('show函数成功执行!')

show(1)  # 函数参数个数不符合预定义，无法执行函数
show(1,2) # show函数成功执行!
show(1,2,3)  # 函数参数个数不符合预定义，无法执行函数
```

### 4、del
`__del__`用于当对象的引用计数为0时自动调用。
`__del__`一般出现在两个地方：1、手工使用del减少对象引用计数至0，被垃圾回收处理时调用。2、程序结束时调用。
`__del__`一般用于需要声明在对象被删除前需要处理的资源回收操作

```python
# 手工调用del 可以将对象引用计数减一，如果减到0，将会触发垃圾回收

class Student:

    def __del__(self):
        print('调用对象的del方法，此方法将会回收此对象内存地址')

stu = Student()  # 调用对象的__del__方法回收此对象内存地址

del stu

print('下面还有程序其他代码')
```

```python
class Student:

    def __del__(self):
        print('调用对象的del方法，此方法将会回收此对象内存地址')

stu = Student()  # 程序直接结束，也会调用对象的__del__方法回收地址
```

### 5、iter、next

这2个方法用于将一个对象模拟成**序列**。内置类型如列表、元组都可以被迭代，文件对象也可以被迭代获取每一行内容。重写这两个方法就可以实现自定义的迭代对象。
```python
# 定义一个指定范围的自然数类，并可以提供迭代

class Num:
    def __init__(self, max_num):
        self.max_num = max_num
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.max_num:
            self.count += 1
            return self.count
        else:
            raise StopIteration('已经到达临界')

num = Num(10)
for i in num:
    print(i)  # 循环打印1---10
```


### 6、getitem、setitem、delitem
重写此系列方法可以模拟对象成列表或者是字典，即可以使用`key-value`的类型。

```python
class StudentManager:
    li = []
    dic = {}

    def add(self, obj):
        self.li.append(obj)
        self.dic[obj.name] = obj

    def __getitem__(self, item):
        if isinstance(item, int):
            # 通过下标得到对象
            return self.li[item]
        elif isinstance(item, slice):
            # 通过切片得到一串对象
            start = item.start
            stop = item.stop
            return [student for student in self.li[start:stop]]
        elif isinstance(item, str):
            # 通过名字得到对象
            return self.dic.get(item, None)
        else:
            # 给定的key类型错误
            raise TypeError('你输入的key类型错误!')

class Student:
    manager = StudentManager()

    def __init__(self, name):
        self.name = name

        self.manager.add(self)

    def __str__(self):
        return f'学生: {self.name}'

    __repr__ = __str__


stu1 = Student('小明')
stu2 = Student('大白')
stu3 = Student('小红')
stu4 = Student('胖虎')

# 当做列表使用
print(Student.manager[0])  # 学生: 小明
print(Student.manager[-1])  # 学生: 胖虎
print(Student.manager[1:3])  # [学生: 大白, 学生: 小红]

# 当做字典使用
print(Student.manager['胖虎'])  # 学生: 胖虎
```

### 7、getattr、setattr、delattr
当使用`obj.x = y`的时候触发对象的`setattr`方法，当`del obj.x `的时候触发对象的`delattr`方法。
当尝试访问对象的一个不存在的属性时 `obj.noexist` 会触发`getattr`方法，`getattr`方法是属性查找中优先级最低的。
可以重写这3个方法来控制对象属性的访问、设置和删除。
**特别注意：如果定义了getattr，而没有任何代码（即只有pass），则所有不存在的属性值都是None而不会报错,可以使用super().__getattr__()方法来处理**

```python
class Student:
    def __getattr__(self, item):
        print('访问一个不存在的属性时候触发')
        return '不存在'

    def __setattr__(self, key, value):
        print('设置一个属性值的时候触发')
        # self.key = value  # 这样会无限循环
        self.__dict__[key] = value

    def __delattr__(self, item):
        print('删除一个属性的时候触发')
        if self.__dict__.get(item, None):
            del self.__dict__[item]

stu = Student()
stu.name = 'zlw'  # 设置一个属性值的时候触发
print(stu.noexit)  # 访问一个不存在的属性时候触发 , 返回'不存在'
del stu.name  # 删除一个属性的时候触发
```

### 8、getatrribute
这是一个**属性访问截断器**，即，在你访问属性时，这个方法会把你的访问行为截断，并优先执行此方法中的代码，此方法应该是属性查找顺序中优先级最高的。
**属性查找顺序：
实例的getattribute-->实例对象字典-->实例所在类字典-->实例所在类的父类(MRO顺序）字典-->实例所在类的getattr-->报错**

```python
class People:
    a = 200

class Student(People):
    a = 100

    def __init__(self, a):
        self.a = a

    def __getattr__(self, item):
        print('没有找到:', item)

    def __getattribute__(self, item):
        print('属性访问截断器')
        if item == 'a':
            return 1
        return super().__getattribute__(item)

stu = Student(1)
print(stu.a)  # 1
```


### 9、enter、exit
这两个方法的重写可以让我们对一个对象使用`with`方法来处理工作前的准备，以及工作之后的清扫行为。
```python

class MySQL:
    def connect(self):
        print('启动数据库连接，申请系统资源')

    def execute(self):
        print('执行sql命令，操作数据')

    def finish(self):
        print('数据库连接关闭，清理系统资源')

    def __enter__(self):  # with的时候触发，并赋给as变量
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # 离开with语句块时触发
        self.finish()

with MySQL() as mysql:
    mysql.execute()

# 结果:
# 启动数据库连接，申请系统资源
# 执行sql命令，操作数据
# 数据库连接关闭，清理系统资源
```
