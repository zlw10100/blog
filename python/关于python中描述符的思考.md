## 重要的python语言特性
描述符应该是python中比较重要的语言特性。它的逻辑类似于：对象“属性访问”时的拦截器。因为使用python编写OOP的代码非常多，其中涉及到很多“属性访问”，所以描述符的应用场景比较广泛。同时，初学python的话，对描述符的理解会相对困难，但是若可以熟练运用描述符，就可以完成很多强大、高可读、灵活的功能设计。

## 描述符的组成
“拆解”一下描述符，大概有这么几点内容：
- 描述符类，描述符实例。描述符是一种统称，对于描述符类而言，关注三个函数接口：`__get__`，`__set__`，`__delete__`。对于描述符实例而言，关注它被定义的位置：类属性。
- 对象的“属性访问”流程，即当我们执行obj.attribute的时候，是向python发起访问对象obj的attribute属性的请求，这个请求将会有多个查找步骤。
- 描述符的操作对象，描述符操作两个对象：类对象和实例对象。

## 描述符的使用
描述符的使用方法是：将描述符实例化对象作为某一个业务类的类属性。
描述符的使用和理解其实并不难，它有3个接口，第一接口是`__get__`，语义是：当实例对象访问某一个属性的时候，如：obj.name，若此name属性是：1、类属性，2、描述符实例，则被描述符实例拦截，执行描述符实例对象的`__get__`方法并将返回值作为属性访问的返回值。
用伪代码表示就是：
```python3
obj.name = name.__get__() if (name is 描述符实例) and (name is 类属性)
```
当访问`__get__`方法的时候，有两种情况：
1. 如果是某一个实例对象访问，则将此实例对象作为方法的instance传入，将此实例对象所属的类对象作为owner传入。（2个参数都有值）
2. 如果是某一个类对象访问（因为是类属性，所以也可以通过类对象来调用），则将此类对象作为owner传入，而instance参数为None。

就像如下代码：

```python3
class D(object):
	def __get__(self, instance, owner):
		print('get', instance, owner)
		return instance.__dict__['name']

class Student(object):
	d = D()

	def __init__(self):
		self.name = 'zlw'

name1 = Student().d
# 'get' <__main__.Student object at ...> <class '__main__.Student'>
# 当被实例对象调用描述符的时候，instance和owner都不为None

name2 = Student.d
# 'get' None <class '__main__.Student'>
# 当被类对象调用描述符的时候，instance是None
```

所以，可以通过描述符，来控制对一个对象的属性的“get访问“，就像一个拦截器。

描述符的第二个接口是`__set__`，这个接口的语义是：当对实例对象的属性进行赋值时，如：obj.name = 'zlw'，若此name属性是一个描述符，则调用描述符的`__set__`函数。
这个接口和上面那个`__get__`接口类似，只不过传入的参数略微有变化，就像如下代码：

```python3
class D(object):
	def __get__(self, instance, owner):
		print('get', instance, owner)
		return instance.__dict__['name']

	# 新增接口
	def __set__(self, instance, value):
		print('set', instance, value)
		instance.__dict__['name'] = value

class Student(object):
	d = D()

	def __init__(self):
		self.name = 'zlw'

Student().d = 'new_name'
# set <__main__.Student object at ...> new_name
```

所以，可以通过描述符，控制对一个对象的属性的“set赋值”。

描述符的第三个接口是`__delete__`，接口语义：当你执行`del obj.name`的时候调用此接口。它只有一个instance参数，代表实例化对象，此接口用的并不多，接口使用方式和上述两个接口大同小异。


## 为什么说描述符很重要？
- 函数对象，是描述符，所以当它被定义为类的实例方法时（等价于成为类属性），可以将实例对象作为函数第一个参数传入，这就是自动传instance作为self的解释。
- property（也称为属性），是描述符，当你对这种属性执行get、set、delete的时候，也是被那三个接口所拦截。
- classmethod、staticmethod，是描述符，当你对这些函数执行操作的时候，会自动帮你传入owner作为cls，或者既不传入instance也不传入owner，这样就实现了statimethod。此外，它们还是装饰器。

所以，描述符的重要并不是业务自身的逻辑和接口很复杂，而是因为很多其他特性都基于此技术。
对于描述符的深入理解，也可以加深对其他特性的理解，因为换句话说，基于描述符的其他特性很多都可以被看成是语法糖。