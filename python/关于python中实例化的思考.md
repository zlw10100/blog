## 什么是类？
python教材中说，类是对象的“模板”，类是对象的“工厂”，对象的产生必须由所属的类进行实例化。有很长一段时间，我一直无法搞明白类和对象、实例之间的关系。它们让我觉得面向对象风格的编程非常难学。
现在，我是这样理解类的：
1. 类和实例，本质上没有区别，都是内存中的一个“对象”。
2. 类和实例，在功能上有所区别。类在功能上定义了如何实例化一个实例，以及实例可以共享的属性等。实例在功能上更多用于业务操作。
3. 简单来说，类是一个约束其他对象的属性/行为的对象。
4. 类和实例，是面向对象编程风格的常用操作（其实就是关注点不同，比如函数式编程的关注点在函数上）。
5. 因为类是一个对象，所以元类用于实例化类，并定义类的行为。元类可以修改类的行为，这种修改，在一般的编码工作中不会用到，所以看起来像深度定制类行为。
6. 所以元类也只不过是一个对象，它对类的操作，就像类对实例的操作一样。
7. 所以本质上没有类和实例的区别，所有“东西”都是对象，只是在功能上做了区分。

## 创建类以及实例
像下面的代码，创建一个学生类，以及创建一个学生实例：
```python3
class Student(object):
    def __ini__(self, name, age):
        self.name = name
        self.age = age

student_a = Student('zlw', 27)
print(student_a.name, student_a.age)
```
这里可以认为定义了两个对象：类对象Stduent，以及实例对象student_a。这两者，本质没有什么不同，只是在功能上有所区别：
- 类对象Student用于创建很多类似student_a这样的实例化对象，并定义一些可以让他们共享的属性和方法。
- 实例对象student_a一般用于业务操作，比如执行属性的判断、修改，方法的调用等等。

## 实例化过程
实例化过程对应的代码是：`student_a = Student('zlw', 27)`，这里代表着几点内容：
- Student是一个callable的对象，这意味着Student一定有一个`__call__`方法（有的，在它的元类中）。
- Student的`__call__`方法一定返回一个实例对象，这个实例对象是向内存申请新开辟的对象（类似c的malloc）。
- Student的`__call__`方法中包含2个操作：向内存申请新对象，以及初始化此对象。这两个操作分别对应：`__new__`和`__init__`接口。
- Student可以自定义`__new__`和`__init__`，它们就是“构造函数”和“初始化函数”，还有一个`__delete__`叫做“析构函数”。
- student_a和Student是两个不同的对象，student_a保留一个指针引用Student。

## 单例模式
特别的，某对象有且仅有一个，则使用单例模式。
教程和网络上给出了几种python中单例模式的写法。

### 引用全局变量
```python3
# students.py
class SingletonStudent(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

single_student = SingletonStudent('zlw', 27)

# main.py
from students import single_student

print(single_student.name)
```
思路：把单例模式写到一个模块文件中，并实例化一个全局变量single_student。业务模块**仅引用**此全局变量以模拟单例。
思考：这是以前我的一些老师的写法，写起来简单粗暴好理解，我也这样使用过。但**这是绝对错误的写法**，因为你无法保证其他模块不会引用SingletonStudent来完成实例化（仅靠约定是没有用的）。

## 引用全局变量且删除类
就是在上一种写法中，在students.py最后追加一句：
```python3
del SingletonStudent
```
思路：这样就可以把原始的类对象删掉，其他模块就不会有机会重新实例化一个新的对象。
思考：咋一看好像可以解决上面那种写法的缺陷。但是**实际上却带来更大的问题，这也是错误的写法**。首先，你再也无法引用SingletonStudent对象，否则会抛出`importError`。其次，这种写法的语义不优雅，studengs.py的逻辑就是先搞出一个SingletonStudent，在实例化完成后删掉，就像“过河拆桥”那样，这种定义了类然后立即删掉的语义不优雅。

## 重写`__new__`方法
因为单例的核心逻辑在于，让构造函数要么仅执行一次，要么每次都返回同一个对象。所以很自然的想到重写构造函数，大概类似这样：
```python3
class SingletonStudent(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, name, age):
        self.name = name
        self.age = age

s1 = Student('zlw', 27)
s2 = Student('zlw', 28)
print(s1 is s2)  # True
```
这种写法可以控制构造函数仅返回一个实例，但是有一个**明显的缺陷：无法防止此实例被多次初始化**，上面代码的s1和s2是同一个对象，但是age属性却被多次初始化。此外，还有一个小缺陷，就是你的确可以访问_instance并修改，虽然按照约定你不应该这样。

## 重写元类的`__call__`方法
```python3
class SingletonStudentMeta(type):
    _instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            new_instance = object.__new__(self)
            self.__init__(new_instance, *args, **kwargs)
            self._instance = new_instance
        return self._instance

class SingletonStudent(object, metaclass=SingletonStudentMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age

s1 = SingletonStudent('zlw', 27)
s2 = SingletonStudent('zlw', 28)
print(s1 is s2)  # True
print(s1.age, s2.age)  # 27, 27
```
这种写法我觉得是目前最合适的写法。
