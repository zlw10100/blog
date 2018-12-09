[TOC]


##一、对象属性的访问控制
看一下这个例子，我们创建一个学生类，提供名字和年龄的属性，然后实例化一个对象，并显示他的信息。

```python
class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age


stu = Student('zlw', 26)
print(stu.name)  # 名字是'zlw'
print(stu.age)  # 年龄是26

# 对象的名字和年龄被正常打印，good
```

```python
# 但是，Student类没办法控制用户在实例化时的行为

stu = Student(26, 'zlw')
print(stu.name)  # 名字是26
print(stu.age)  # 年龄是'zlw'

```
我们可以这样做：
```python

class Student:

    def __init__(self, name, age):
        # 检测每一次实例化时的参数类型
        if not isinstance(name, str):
            raise TypeError('name必须是str类型')
        if not isinstance(age, int):
            raise TypeError('age必须是int类型')

        self.name = name
        self.age = age
```
我们可以在init函数中控制实例化时的输入类型，不过这有2个问题：
1、只能控制实例化时的类型，对于已经实例化完成的对象，可以直接通过stu.name = 23的形式来重新赋值
2、实例化传递的参数越多，那么类型检测的代码也越多，而且类型检测代码和初始化代码写在一起，两者干的事情不一样，逻辑不是一个层面的，都写在init函数里并不合适
我们可以这样写：
```python
# 省略了age的处理，方式是一样的

class Student:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError('name属性值类型必须是str类型')

        self.__name = name


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('name属性值类型必须是str类型')
        self.__name = value

# 这样写就可保证在实例化和已经完成实例化的对象赋值时的类型检查问题了。
# 不过还是有一个问题，就是属性越多，这个类型检查的代码就会不断增加，并且堆积在Student类中
# 我们应该将类型检查的代码单独隔离开，但同时又可以和Student类进行交互
```
使用python的描述符来处理。

##二、描述符基本理解
python的描述符，有几个理解：
>1、描述符是一个类
>2、描述符的目的是对属性的访问控制
>3、描述符将访问控制和业务类分离开，业务类处理业务逻辑，描述符处理属性访问控制
>4、描述符是一个特殊类型的类，所谓特殊，就是自定义了`__get__`、`__set__`、`__delete__`方法的类，这种类就叫描述符
>5、单独一个描述符没有啥意义，描述符要作用于某一个具体的业务类，为这个业务类提供属性访问控制的功能
>6、属性访问可不仅仅是指数据属性的访问，对于函数属性的访问也可以控制。
>7、使用类的`__setattr__`、`__getattr__`、`__delattr__`只能全局控制所有属性，而描述符可以有针对的控制部分属性

##三、基本使用

```python

class DescName:
    dic = {}

    def __init__(self, value_type):
        self.value_type = value_type

    def __get__(self, instance, owner):
        print('get running...')
        return self.dic.get(instance, None)

    def __set__(self, instance, value):
        print('set running...')
        if not isinstance(value, self.value_type):
            raise TypeError('名字必须是str类型')

        self.dic[instance] = value

class Student:
    name = DescName(str)

    def __init__(self, name, age):
        self.name = name
        self.age = age

stu1 = Student('小明', 26)
print(stu1.name, stu1.age)  # 小明，26
stu2 = Student('小红', 25)
print(stu2.name, stu2.age)  # 小红，25
```
上方代码中，我定义了一个`Student`类用于表示一个学生。学生有两个属性`name`和`age`，对于`age`我并没有设置任何的控制，对于`name`我要求属性值必须是`str`类型。我们可以定义一个`DescName`描述符类来单独针对`name`这个属性提供控制功能。`DescName`描述符会对`name`的值进行类型判定，如果是非`str`类型就会报错。
请注意`DesnName`的`__set__`方法中的：`self.dic[instance] = value`这句代码。
考虑到`Student`类会实例化出很多不同的学生对象，这些学生对象是共享同一个描述符对象`Student.name`的，因为这是一个类属性，我们要在`DescName`描述符中保存不同对象的`name`值，就需要区分不同的对象，我这里使用字典，将每一个实例作为字典的`key`来保存对应实例的`name`值。
不过这里也会有一个问题，就是字典的`key`必须是可`hash`对象，如果实例是可变对象比如`list`，则无法使用这种方法保存属性值，可以考虑转换成一个不可变对象后处理，比如使用字符串表示不同的实例对象。

> 基本使用的代码中，每个实例对象的属性值实际是保存在共享描述符对象中的。

##四、使用描述符完成property、classmethod、staticmethod自定义实现

###1、property的自定义实现
```python
# property是一个装饰器，所以底层原理就是把描述符当做一个装饰器并作为类属性存在

class DescName:  # 描述符，后续当做装饰器使用，是一个类装饰器，返回的对象是描述符对象
    def __init__(self, func):  # 首次装饰必须返回一个描述符对象，func是装饰的函数name
        self.get_func = func
        self.set_func = None
        self.delete_func = None  # 以上3个属性用于保存用户定义的属性访问逻辑代码

    def __get__(self, instance, owner):
        return self.get_func(instance)  # 访问get的时候返回用户定义的函数输出

    def setter(self, func):
        self.set_func = func
        return self  # 提供一个setter用于处理set逻辑，setter是一个函数装饰器

    def __set__(self, instance, value):
        return self.set_func(instance, value)  # 访问set的时候调用用户定义函数

    def deleter(self, func):  # 提供deleter函数装饰器处理delete逻辑
        self.delete_func = func
        return self

    def __delete__(self, instance):
        return self.delete_func(instance)  # 访问del的时候调用用户定义函数


class Student:  # 业务类
    def __init__(self, name, age):
        self.__name = name  # 在业务类中隐藏属性
        self.age = age

    @DescName  # 和propery是一样的,返回对象就是一个描述符对象，被name引用,且是类属性
    def name(self):
        return self.__name

    @name.setter  # set设置
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('必须是str')
        self.__name = value

    @name.deleter  # 删除设置
    def name(self):
        print('你不能删除名字属性')

stu1 = Student('zlw', 26)  # 实例化的时候会自动调用描述符的set
print(stu1.name, stu1.age)  # 打印的时候会调用描述符的get

stu1.name = 'wj'
print(stu1.name, stu1.age)

del stu1.name  # 删除的时候调用描述符的delete
```

###2、classmethod的自定义实现
```python

class DescClassMethod:  # 描述符，用于作为装饰器，提供类方法功能
    def __init__(self, func):
        self.get_func = func
        self.cls = None  # 保存当前类对象

    def __get__(self, instance, owner):  # 被装饰的时候，保存当前类对象，返回描述符对象
        self.cls = owner
        return self

    def __call__(self, *args, **kwargs):  # 类方法一般直接运行，也就是描述符对象被运行
        return self.get_func(self.cls, *args, **kwargs)  # 传入当前类对象，用户就觉得是自动传入


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def learn(self):
        print(f'{self.name} is learning...')

    @DescClassMethod  # 类方法描述符，让被装饰的函数变成类绑定方法，自动传入类对象
    def show_class(cls, school_name):
        print(f'this is class --> {cls.__name__}')
        print('输入的参数是:', school_name)

stu = Student('zlw', 26)
stu.learn()  # 实例方法
Student.show_class('北京大学')  # 类方法
```

###3、关于实例方法的思考

```python
# 这里是普通的类和一个实例方法定义，不同对象在调用的时候会将自己传入self

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def learn(self):
        print(f'{self.name} is learning...')

stu1 = Student('小明', 26)
stu2 = Student('小红', 25)

stu1.learn()  # '小明' is learning...
stu2.learn()  # '小红' is learning...
```
通过描述符，我们可以实现一个类似`classmethod`类方法的功能，这功能可以实现当我们调用类方法的时候，`python`会自动将类对象传入`cls`中。那这就引发另一个问题，对于实例方法，我们在通过实例对象调用的时候，也会将实例对象自己传入`self`中，那这个实现和类方法的实现，是不是一样的思路？
仔细查看描述符的`__get__`函数可以发现，此函数的参数有`instance`和`owner`，这个`owner`被我们用作`cls`，那么，`instance`不就代表实例对象吗？如果我们把`istance`传入`call`，不就可以实现类似实例方法的功能了吗？试试看：

###4、实例方法的自定义实现

```python
class SelfMethod:  # 描述符，用于处理实例方法功能
    def __init__(self, func):
        self.get_func = func
        self.instance = None  # 保存实例对象

    def __get__(self, instance, owner):
        self.instance = instance  # 保存实例对象
        return self

    def __call__(self, *args, **kwargs):
        return self.get_func(self.instance, *args, **kwargs)  # 将实例对象传入


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @SelfMethod  # 使用描述符作为装饰器，让learn函数变成实例绑定方法
    def learn(self):
        print(f'{self.name} is learning...')

stu1 = Student('小明', 26)
stu2 = Student('小红', 25)

stu1.learn()  # '小明' is learning...  # 调用的时候，会传入stu1实例
stu2.learn()  # '小红' is learning...  # 调用的时候，会传入stu2实例

print(stu1.__dict__)
print(Student.__dict__)  # 类中显示learn是一个描述符对象
```
以上通过描述符可以自定义类似实例方法的效果，自动传入实例给`self`。不过这种实现方式和真正的实例方法实现（暂时还不知道如何实现的）还是有些不同：
>a、自定义实现需要@SelfMethod装饰器，而真正实现是不需要装饰器的，不知道是不是底层做了默认省略的操作
>b、`Student.__dict__`的输出中，自定义的实现表示`learn`是一个描述符对象，而真正实现的表示是一个`function`对象
>c、打印`stu1.learn`的时候，自定义实现显示是描述符对象，真正实现表示的是绑定方法对象

嗯。。暂时还没深入研究绑定方法的具体实现，不过可以通过描述符来大概判断出，绑定方法也应该是一个类似封装了实例对象和函数的对象，在被调用的时候也是以`func(self, *args, **kw)`的方式来调用的。

###5、静态方法的自定义实现
```python
class StaticMethod:  # 描述符，用于处理静态方法的类装饰器
    def __init__(self, func):
        self.get_func = func

    def __get__(self, instance, owner):
        return self

    def __call__(self, *args, **kwargs):
        return self.get_func(*args, **kwargs)  # 静态方法就是不提供instance和owner参数传入


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @StaticMethod  # 描述函数为静态方法
    def show():
        print('这里是静态方法show')

stu1 = Student('小明', 26)
stu2 = Student('小红', 25)

stu1.show()  # 这里是静态方法show
stu2.show()  # 这里是静态方法show
```

##五、总结

>1.描述符可以用于处理类级别的属性的访问控制
>2.如果描述符处理的是数据属性，那么核心关注点如下
    >1、描述符的`__get__`,`__set__`,`__delete__`函数处理数据读取、删除
    >2、处理数据属性的描述符对象，可以保存不同实例对象的属性值，使用字典，`key`是实例对象自身，不过要注意是否可`hash`
    >3、将描述符作为类装饰器对函数进行装饰，可以自定义类似`property`的`get`实现效果，不过注意描述符类中要提供`setter`和`deleter`用于处理`set`和`del`

---

>描述符还可以用于处理函数属性，核心关注点有如下
    >1、描述符类作为类装饰器对指定函数进行装饰并返回描述符对象
    >2、返回的描述符对象除了处理描述符三大函数之外，还要提供`__call__`函数以便调用
    >3、使用`__call__`函数的时候，传入的是`instance`，就类似实例方法，传入的是`owner`，就类似类方法`classmethod`，什么都不传入，就类似静态方法`staticmethod`。

---

>对象属性的解析顺序，比如打印`stu.name`
0、无条件优先被`__getattribute__`处理
1、获取对象所属类及`MRO`列表，自下而上获取`name`的第一个定义
2、判断此定义的类型
3、如果类型是数据描述符，直接调用数据描述符的`__get__`，否则下一步
4、如果不是数据描述符，判断是否为：实例属性，即`stu.__dict__`中是否存在，是的话返回，否则下一步
5、判断类型是否为非数据描述符（也是描述符），如果是，则返回非数据描述符的`__get__`返回值，否则下一步
6、判断类型是否是普通属性，比如单纯的一个类属性，如果是，则返回此属性值，否则下一步
7、执行`__getattr__`，期望解析顺序最后给出返回值，没定义就报错