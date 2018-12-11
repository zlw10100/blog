

[TOC]




# 一、基本知识点
## 1、面向过程编程
1. 视角聚焦于解决问题的步骤，特点是每一步的行为都基本固定，且强烈依赖于上下文。一旦程序编码完毕，程序内部各步骤代码就形成一个强相关的整体，不方便频繁的修改和扩展。

2. 这种编码形式在编码前会明确解决问题的各个步骤并分解至最简单的语句，故编码较为简单。

3. 面向过程的程序代码一般适用于不会经常变动代码内容的场景，或者是在程序中的某一个部分使用面向过程编码，这样即使发生了需求变动，也只需要重写这一部分较少的代码。

- [x] 面向过程编程标签
        - [x] 简单
        - [x] 固定
        - [x] 依赖上下文(耦合强)
        - [x] 重写
        - [x] 适合小场景

## 2、面向对象编程
1. 站在上帝视角，对全局设计和建模。

2. 上帝创造出程序中的对象，不同对象有着独特的属性、特征、功能，对象之间相互作用一起支撑程序的运行。

3. 因程序的运行完全来源于对象之间的交互，所以上帝也无法明确程序的每一个步骤。

4. 面向对象编程的代码一般适用于经常变动代码内容的场景，通过此种编程方式产出的代码，模块间不会有很强的耦合性，这就提供了可以灵活更换、修改、扩展模块的能力。

- [x] 面向对象编程标签
        - [x] 复杂
        - [x] 灵活
        - [x] 模块化(低耦合)
        - [x] 可插拔
        - [x] 适合大规模

## 3、注意
> 1. 面向过程和面向对象只是对一个程序的设计视角和模式不同，两者各有优缺点，并没有哪一种是绝对的优秀而要抛弃另一种。
> 2. 我觉得良好的程序设计应该是在合理的场景使用合理的编程模式，一个优秀的程序应该是可以支持混合编程，在程序代码的不同阶段、不同角度、不同抽象层次使用对应最适合的编程模式，各种编程模式相辅相成协作完成程序的正确执行。

---

# 二、类的结构
## 1、类的理解
1. 不论是程序世界还是现实世界，类都是对于一个有着相似特征、属性、功能的象集合体的描述。

2. 一般我们以特征和功能来描述一个对象，如：
我们描述一个人，会说他有耳朵鼻子嘴巴四肢...，同时，他还可以开车、吃饭、聊天、看电影...

3. 对象的长相，或者说特征(或者说可以被看到的属性)是对象的描述之一。

4. 对象的能力、功能、行为(对象可以做的事情)是对象的描述之二。

5. 而多个相同对象应该有着相同或者相似的特征和功能(否则也不会被划分成一个类别了)，这些相似的属性和功能就是这类对象的描述。

6. 而反过来说，如果知道一类对象的描述，那么上帝完全可以通过这些描述信息，创建一个属于此类的对象。

> **多个对象----->一个类别描述，这叫抽象**

> **一个类别描述----->多个(一个)对象，这叫实例化**

## 2、代码形式
```python
class Student(object, metaclass=type):
    count = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_name(self):
        print('my name is:', self.name)
```
类代码可以**暂时**的理解成有如下几个部分

- [x] 1、`class`关键字（必须）
- [x] 2、类名`Student`（必须）
- [ ] 3、继承类列表`object`（可不写）
- [ ] 4、元类指定`metaclass=type`（可不写）
- [x] 3、类体（必须有，但可以是`pass`）
    - [ ] 以下为类体中可以包含的内容：
    - [ ] 5、类数据属性（可不写）
    - [ ] 6、构造函数`__init__`（可不写）
    - [ ] 7、普通对象绑定方法`show_name`，也叫实例方法（可不写）

所以一个**最最简单**的类代码就像这样
```python
class Student:
    pass
```

## 3、类和函数的一些区别
函数

:   1. `python`解释器在**编译代码**的时候只会在命名空间中声明函数引用和函数对象的创建，**不会执行函数体**，函数体中的局部变量也不会被创建。
2. **当函数被执行时**，**执行函数体**中的代码，局部命名空间被创建，局部变量随之创建。

类

:   1. `python`解释器在**编译代码**的时候会在命名空间声明类引用和类对象的创建，**会执行类体代码**，并创建此类的命名空间，命名空间作为类对象`的__dict__`属性值。
2. 如果类中的代码是函数定义或者其他变量定义，则执行声明定义，如果代码是执行语句（如`print`）则执行此语句。
3. **当类被执行时**，如：`Student()`，类**不会执行类体代码**，而是返回一个此类的**实例化对象**，返回对象的过程叫做实例化。

## 4、类中的数据

对象的属性保存在对象的__dict__字典中，可以通过 对象.属性名 的方式来访问和修改。

类也是一个对象，类在定义时，类体中定义的数据即为类对象的属性，可以通过 类名.数据名 的方式来访问和修改，如：

```python
class Student:
    a = 2

print(Student.a)  # a = 2

Student.a = 44
print(Student.a)  # a = 44

del Student.a
print(Student.a)  # 报错 AttributeError: type object 'Student' has no attribute 'a'
```

## 5、类中的方法(基础)
类中的方法就是一个普通的函数定义，此函数属性也保存在类对象的__dict__字典中，和数据属性一样，可以通过 类名.函数名 的方式来访问和修改，如：
```python
def say(self):
    print('全局的say方法, hi!')

class Student:
    a = 2

    def say(self):
        print('类里面的say方法, hello!')


Student.say('something')  # 类里面的say方法, hello!

# 类中函数属性可以重新赋值
Student.say = say
Student.say('something')  # 全局的say方法, hi!

del Student.say
Student.say('something')  # AttributeError: type object 'Student' has no attribute 'say'
```
**注意：
1、类中定义的任何函数（默认情况下）都必须固定第一个self参数的存在，所以如果是以类为主体使用类中的函数时，就必须给self参数传递一个值，不论这个值是什么。
2、类可以当做是一个容器对象来保存数据。**

---

# 三、类的实例化
类的另一个非常重要的作用是：实例化对象。
```python
class Student:
    school = '北京大学'

    def __init__(self, name, age):
        self.name = name
        self.age = age

stu1 = Student('stu1', 26)
stu2 = Student('stu2', 22)

print(stu1)  # <__main__.Student object at 0x000001F1E8E780B8>
print(stu2)  # <__main__.Student object at 0x000001F1E8E780F0>

print(stu1.school)  # 北京大学
print(stu2.school)  # 北京大学

print(stu1.name, stu1.age)  # stu1 26
print(stu2.name, stu2.age)  # stu1 26
```
>1、类可以被执行，执行时传入的参数与`__init__`函数参数对应（不用传self）

>2、类执行的结果是一个对象，有内存地址

>3、类执时传入参数的目的是为了初始化这个实例化对象的某些属性值（当然也可以不初始化，在后续配置）

>4、类中的数据属性，被所有此类对象共享`'北京大学'`

>5、类中的函数属性，默认是绑定到对象的，即每个对象都有一个绑定方法，此方法的执行代码指向类中的此函数

>6、每一个对象都有自己的属性值，通过 对象.属性名 来访问和修改

>7、类实例化的目的是为了得到一个对象，程序中有了对象之后就可以相互交互，完成程序的执行。

对象使用绑定方法
>1、对象在创建时，python会将类中的普通方法做一些处理，然后绑定到对象身上。

>2、对象在使用这些绑定方法的时候，会自动的将对象本身传入到此方法的第一个self参数中，这样就可以在函数中引用到此对象。

>3、绑定方法是将函数和对象绑定在了一起，只要绑定方法被调用，就会自动传入对应的对象。

---

# 四、类的继承
## 1、MRO
```python
class Animal(object):
    pass

class People(Animal):
    pass

class Student(People):
    pass

print(Student.mro())
print(Student.__mro__)  # 二者等价，唯一的区别是上面结果是列表，下面是元组

# 返回结果：
# [<class '__main__.Student'>, <class '__main__.People'>, <class '__main__.Animal'>, <class 'object'>]
# (<class '__main__.Student'>, <class '__main__.People'>, <class '__main__.Animal'>, <class 'object'>)
```
>1、类可以继承，即如果我们把多个类的相同之处再提取出来，就可以再次抽象出一个类，此类作为其所有子类的父类。

>2、继承就类似家族树、学科专业目录、动物类别，最顶层的是最抽象的类别，越往下走，类别越清晰，继承树的末端就是各个具体的对象。

>3、我们可以使用MRO来表示一个类它向上方向的父类路径，MRO是一个通过算法计算得到的父类元组。

>4、任何一个类的MRO都可以表示它在继承树中的位置。

MRO的用处

**MRO可以确定搜索路径**

子类一旦继承父类，就会自动继承父类的所有代码定义（实际并没有直接得到，而是通过MRO搜索得到）

继承的好处是子类不需要重复编写和父类相同的代码，同时继承也可以很明确的表示出**什么是什么**的结构关系，坏处是继承使用的越多，这个继承树上的耦合性越强，因为一旦顶层类发生了变动，下方所有子类都会受到影响。


## 2、派生、调用、重写

子类自动继承父类的所有代码。
子类可以在此基础上新增自己的代码，这叫派生，子类的代码又会被自己的子类所继承。
子类可以通过super()函数来调用上一级父类的属性，注意，仅仅是向上一级，依赖于继承树。
子类也可以通过 父类名.属性名 的方式来调用父类的属性，不依赖于继承树。
子类也可以重写覆盖父类的代码，此时将会以子类提供的属性值为准。

## 3、super()

子类通过super()来调用上一级父类的属性。
通过 父类名.属性名 的方式调用任何一级父类的属性。
当有多继承，即有多个父类的情况下，super()函数的上一级父类是哪一个取决于MRO中的搜索路径。

## 4、属性查找顺序
函数
>函数内部变量的访问原则是：LEGB

>函数局部---嵌套函数局部(如有嵌套)---全局空间---内置空间--报错

类

>对象访问一个属性的原则是

>对象`__dict__`---类`__dict__`---父类`__dict__`---基类object`__dict__`---元类`__dict__`---报错

```python
class MyMeta(type):
    a = 100
    pass

class Animal(object):
    pass

class Student(Animal, metaclass=MyMeta):
    pass

print(Student.a)  # a = 100
```

## 5、广度和深度优先
>python2中的旧式类（即没有继承object的类及其子类）使用深度优先。
python2和python3的新式类使用广度优先。

>深度优先就是最长继承路径优先搜索。
广度优先，从左向右开始，搜索到有共同父类的前一个类放弃当前搜索路径。

---

# 五、抽象类
## 1、规则
抽象类用于规定子类们相同功能的函数接口

抽象类提供抽象方法定义，但是并不实现

抽象类不能被实例化，只能被继承

抽象类由对多个有着相似属性和功能的类进行抽象得到

子类一旦继承抽象类，必须实现抽象类中定义的抽象方法

python自身没有提供抽象类功能，需要使用abc模块来提供支持

抽象类兼具接口和类的部分特性

抽象类的好处是，明确了类继承的语义，且规范了子类的函数接口，提高了归一化

## 2、抽象类的使用
```python
import abc  # 借助模块实现抽象类功能

class Animal(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod  # 定义接口
    def run(self):
        pass

    @abc.abstractmethod
    def sleep(self):
        pass

class People(Animal):
    def run(self):
        print('running...')  # 子类必须实现，且接口必须严格按照抽象类的定义

    def sleep(self):
        print('sleeping...')

p = People()  # 只有子类可以实例化
p.run()
p.sleep()
```

---

# 六、类的封装功能
## 1、`__xx`私有变量
类的定义中，可以使用形如`__xx`的变量名来隐藏敏感数据，这些变量名会在编译的时候变形成：`类名__xx`的形式存在。使用了这种变形功能后，可以提供一个唯一的数据访问和设置接口来**控制敏感数据的访问**。

这种变形是约定俗成的使用方式，实际上依然可以通过`类名__xx`的方式来访问数据。

**这种变形方式对于数据和函数均可以使用。**

```python
class Student:
    def __init__(self, name):
        self.__name = name

    def __show(self):
        pass

stu1 = Student('stu1')
print(stu1.__dict__)  # {'_Student__name': 'stu1'}
print(stu1.name)  # AttributeError: 'Student' object has no attribute 'name'
```


## 2、property
`property`的主要功能是提供一个伪装，对外的接口是一个普通的属性名，而在内部通过函数执行来访问和设置数据。

`property`可以提供`getter`、`setter`、`deleter`三种数据的访问形式，内部函数可以用于对于数据的访问控制。

`property`也可以用于需要实时执行计算的属性，如三角形面积的计算、人的`BMI`指数的计算。

**一般会将`__xx`和`property`联合使用，因为property需要使用另一个属性名来防止无限递归。**

```python
class Student:
    def __init__(self, name, money):
        self.name = name
        self.__money = money  # 注意，需要使用另一个属性名，否则会无限递归

    @property
    def money(self):
        print(f'这里可以控制{self.name}的money属性访问')
        return self.__money

    @money.setter
    def money(self, new_moeny):
        print(f'这里可以控制{self.name}的money属性设置')
        self.__money = new_moeny

    @money.deleter
    def money(self):
        print(f'这里可以控制{self.name}的money属性删除')
        raise AttributeError('此属性不可删除')


stu1 = Student('stu1', 30000)

print(stu1.money)
stu1.money = 40000
del stu1.money
```

## 3、函数封装
函数封装一般用于隐藏内部实现细节，提供公开统一接口。

隐藏内部细节函数可以提神安全性，因为一旦公开细节函数，就要考虑会被外部用户调用。

应该将一个功能封装成一个公开的接口，对开开放，同时此接口需要做一定的访问控制。

**可以使用__xx的方式来隐藏细节函数，一般在类中也会使用_函数名的方式来表示此函数是内部函数。**

```python
class Student:
    def __init__(self, name, money, password):
        self.name = name
        self.__money = money
        self.__password = password

    def show_money(self, password):  # 对外仅仅提供这个公开接口
        print('这里可以控制访问此函数的权限')

        if password == self.__password:  # 访问控制处理
            return self.__get_money()
        else:
            print('拒绝访问')
            return None

    def __get_money(self):  # 内部实现细节函数，一般无法直接访问
        return self.__money

stu1 = Student('stu1', 30000, '123')
print(stu1.show_money('123'))  # 验证正确，得到敏感数据
print(stu1.show_money('abc'))  # 没有得到敏感数据
```

---

# 七、类中的方法


## 1、绑定方法
### 实例绑定方法
类中定义的函数在默认情况下就是实例绑定方法。在实例化对象的过程中，`python`会将函数与对象绑定形成一个绑定方法。当绑定方法被调用时，会自动传递对象作为第一个`self`参数。
### 类绑定方法
类中定义的函数增加了`@classmethod`装饰器之后将会被定义成类绑定方法，和实例绑定方法类似的，类绑定方法将会把函数与类对象绑定在一起，当类绑定方法被调用的时候，会自动传递类对象作为第一个`cls`参数。
## 2、非绑定方法
类中使用`@staticmethod`装饰器的函数，此时函数作为一个普通的函数存在于类空间中，在使用时必须严格按照普通函数的参数传递方式


# 八、类的内置方法(特殊方法，后补）

# 九、对象实例化过程(简单)
1、通过类名执行调用，如：`Student（）`
2、`Student`类中的`__new__`方法被执行，将`Student`对象传入作为第一个`cls`参数，此方法将会调用父类的`__new__`方法并返回一个对象`obj`
3、在`__new__`方法中，`Student`类中的`__init__`方法被执行，将`obj`对象传入作为第一个`self`参数，此方法返回值固定为None
4、`__new__`方法返回经过`__init__`函数初始化过的对象`obj`，
5、赋值给变量`stu1 = Student（）`

# 十、元类
## 1、使用exec
exec是内置函数，和eval类似，可以执行字符串形式的python代码
exec函数有3个参数：代码、全局空间、局部空间
```python
code = """
a = 2
global b
b = 3

def show():
    print('hello')
"""

g_dic = {}
l_dic = {}

exec(code, g_dic, l_dic)

print(g_dic)  # b的定义
print(l_dic)  # a和show函数的定义
```

## 2、元类的定义
如果一切皆对象，那么python的类也是对象。类对象是如何产生的？

python中的类对象通过元类产生，即：元类产生类对象，类对象再实例化对象。

python中的元类是type，元类产生了所有的python类，最重要的就是type类产了object类，即：通过元类的定义，可以定制object类的内容。

## 3、类的组成要素

类名、继承列表、类体代码

## 4、实例化类对象
元类的执行将会产一个类对象，类对象从元类的`__new__`函数产生，并经过元类的`__init__`初始化属性。

## 5、通过__new__和__init__控制类对象的产生过程

```python
class MyMeta(type):
    def __new__(cls, class_name, class_bases, class_dic):
        print('元类，cls is:', cls.__name__)
        print('现在准备创建类对象:', class_name)
        return super().__new__(cls, class_name, class_bases, class_dic)

    def __init__(self, class_name, class_bases, class_dic):
        print('选择要对类对象初始化', self.__name__)
        self.class_name = class_name
        self.class_bases = class_bases
        self.class_dic = class_dic

        self.a = 2


class Student(object, metaclass=MyMeta):
    pass

print(Student.a)  # 2
```
>元类调用new方法的时候传入的是类的三元素，并返回一个类对象，类对象被传入init方法中，并对此类对象进行初始化

## 6、通过__call__控制类对象实例化对象的过程
```python
class MyMeta(type):
    def __call__(self, *args, **kwargs):
        print('此类正在执行call', self.__name__)

        obj = object.__new__(self)
        self.__init__(obj, *args, **kwargs)
        return obj


class Student(object, metaclass=MyMeta):
    pass

stu1 = Student()

print(stu1)
```
>类对象在实例化的时候，会调用`call`方法（此方法应该是元类给予的），`call`方法将会调用`object`的`new`方法得到一个空对象，然后对此空对象进行初始化，并返回此对象。

## 7、单例模式的使用
### 通过类的new方法操作
```python
class Student:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            obj = object.__new__(cls)
            cls.__init__(obj, *args, **kwargs)

            cls.__instance = obj
        return cls.__instance

stu1 = Student()
stu2 = Student()

print(stu1 is stu2)  # True
```

### 通过元类操作
```python
class MyMeta(type):
    def __init__(self, *args, **kwargs):
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            obj = object.__new__(self)
            self.__init__(obj, *args, **kwargs)
            self.instance = obj
        return self.instance


class Student(object, metaclass=MyMeta):
    pass

stu1 = Student()
stu2 = Student()
print(stu1 is stu2)
```
>个人觉得直接使用类的new操作更方便


# 十一、几个技术问题
## 1、__new__方法

>`new`方法是生成对象的方法，在元类中，使用`type`元类的`new`方法生成类对象。
>在类中，使用`object`的`new`方法生成实例化对象。
>`new`方法应该是调用底层接口在内存中申请一个空间。
>`new`方法会返回一个空对象。

## 2、__init__方法

>`init`方法是对对象进行初始化的方法，在元类中，是对类对象进行初始化，在类中，是对对象进行初始化。`init`方法返回值是 `None`。


## 3、super()调用时传入的都是子类对象
```python
class Animal:
    def f(self):
        print('这里是animal')
        print('self 是:', self)


class People(Animal):
    def f(self):
        print('这里是people')
        super().f()

class Student(People):
    def f(self):
        print('这里是student')
        super().f()

stu1 = Student()

print(stu1)  # 和stu1.f()中的对象是同一个
stu1.f()
```
> super()方法会将子类对象传递给父类

## 4、为啥对象的绑定方法id不同
```python

class Student:
    def eat(self):
        print('eating...')


stu1 = Student()
stu2 = Student()

print(stu1.eat)  # bound method 0x000002C94A04C9E8
print(stu2.eat)  # bound method 0x000002C94A04CA20
```
两个对象，都是使用同一个函数，但是绑定方法地址却不同
绑定方法也是对象，是对普通函数和对象的封装
```python
class Student:
    def eat(self):
        print('eating...')


stu1 = Student()  # __main__.Student object 0x00000192233FC9E8
print(stu1)

bound_func = stu1.eat
print(bound_func.__self__)  # __main__.Student object 0x00000192233FC9E8
print(bound_func.__func__)  # function Student.eat at 0x00000192233F9488
```
>1、绑定方法是一个对象
2、绑定方法将实例化对象和函数对象封装在一起
3、绑定方法在调用的时候应该执行函数对象，并把实例化对象传入给函数self参数

## 5、类是装饰器
### 没有参数的装饰器
```python
class Wrapper:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kw):
        print('start')
        self.func(*args, **kw)
        print('end')

@Wrapper
def show():
    print('这里是show函数')

show()

# start
# 这里是show函数
# end
```
### 有参数的装饰器
```python
class Wrapper:
    def __init__(self, key):
        self.key = key

    def __call__(self, func):
        self.func = func

        def inner(*args, **kw):
            print('start')
            self.func(*args, **kw)
            print('end')
        return inner


@Wrapper('key')
def show():
    print('这里是show函数')

show()

# start
# 这里是show函数
# end
```


## 6、对象的[]和反射的不同
```python
class Student:
    a = 2

print(getattr(Student, 'a'))  # 2，getattr是获取对象的属性

dic = {
    'a': 100,
}
print(getattr(dic, 'a'))  # 报错，字典中的key需要使用dic['a']访问
```