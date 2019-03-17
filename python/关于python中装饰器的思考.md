## 基本语言特性？？？
有些文章和朋友认为装饰器是python中的一个语言特性，这是错的，至于符号@，这只是一种语法接口封装。
单从装饰器自身来说，它最多算一个设计模式。
如果非要说是特性，那应该说闭包（甚至是词法作用域）才是语言特性。

## 我的装饰器学习
我在刚刚开始学习python的时候，教程中、老师中、同学中，都说要深入研究装饰器，这是python优雅的一种表现，是一个功能强大的实现。当时我也花了很大的时间去仔细研究，也有一点点收获（下面我会写），但是现在我已经学了9个月，也算是已经入门，再回头看看，python的装饰器真的。。需要花那么大的精力去研究吗？它本身真的是很高深的技术吗？

## 装饰器的应用场景很有限
受限的原因主要是装饰器的定位，我们经常这样描述一个装饰器：**它在保留原有业务代码不改变的前提下，为业务新增额外的功能。**请注意，这里有两点很重要：
1. 它不改变原有业务代码，这意味着它的代码逻辑无法合并到业务逻辑中。
2. 新增额外的功能，这些功能一般都是业务的辅助功能，而不会是核心功能。

**换句话说：装饰器的目的是增加对业务不那么重要的辅助功能，而不是扩展业务的核心功能，这意味着装饰器的定位是辅助扩展。**

在代码中，我们可以在极少量（相对于其他技术而言）必要的场景中使用装饰器，但却无法继续扩展它的功能，除非你想这样写功能扩展代码：
这里有一个普通的函数，打印名字
```python3
import time

def hello(name):
	time.sleep(1)
	print('hello', name)
```
现在你希望扩展此函数，增加一个计算函数运行时间的功能：
```python3
def show_runtime(func):
	def inner(*args, **kwargs):
		start = time.time()
		result = func(*args, **kwargs)
		end = time.time()

		print('func run time:', end - start)
		return result
	return inner
```
于是使用装饰器的话，代码就是这样：
```python3
@show_runtime
def hello(name):
	time.sleep(1)
	print('hello', name)
```
此时，你又希望增加一个函数运行时记录日志的功能：
```python3
def log(func):
	def inner(*args, **kwargs):
		print('函数被执行，记录日志xxxx')
		result = func(*args, **kwargs)
		return result
	return inner
```
现在代码变成这样了：
```python3
@log
@show_runtime
def hello(name):
	time.sleep(1)
	print('hello', name)
```
如果一直这样使用装饰器增加功能，那最后代码就是这样：
```python3
@...
@login_require
@traffic
@log
@show_runtime
def hello(name):
	time.sleep(1)
	print('hello', name)
```

所以，95%的情况下，都不会去使用装饰器，因为业务的主要逻辑都并入正常代码中，只有少量的代码或者场景适合使用装饰器，才会去使用它。

## 什么时候使用装饰器
需要增加与主体业务基本毫无关系的必要功能时，或者是为了某些特殊的使用方法，比如flask的route注册。
```python3
@app.route('/login/', method=['GET', 'POST'])
def login_view():
	pass
```

## 带参数的装饰器
其实带参数的装饰器，就是至少三层的嵌套函数，每一层都添加一个参数用于表达那一层的逻辑。它们的逻辑可以理解成这样（伪代码）：
```python3
def 最外层(参数)  # 定义最外层的功能逻辑，比如是一个bool参数表示开关
	def 中间层(参数)  # 定义中间层的功能逻辑，一般作为被装饰函数的包裹函数
		def 内层(参数)  # 定义内层功能逻辑，一般定义额外的功能代码
```
比如如果我要定义一个装饰器，为某一个函数增加一个功能，使得调用函数时可以将日志保存到指定文件。
```python3
from functools import wraps

def log_to(filename):
	def mid(func):
		@wraps(func)  # 这一条语句的目的是为了在后续print(add)的时候可以拿到真实add函数的元数据
		def inner(*args, **kwargs):
			print('准备记录日志到:', filename)
			result = func(*args, **kwargs)
			return result
		return inner
	return mid

@log_to('/logs/add.log')
def add(num):
	return num + 1
```
所以按照这种分层的逻辑，我们可以在写出更多层的装饰器，每一层都代表一种逻辑并提供对应的参数即可。

## 使用类作为装饰器
装饰器是一种高阶函数，所以理论上来说，只要对象可以执行call，就可以作为装饰器。
所以不论是类对象，还是实例对象，都可以作为装饰器，而并不仅限于函数对象（前两者可以使用`__call__`函数）。
使用类作为装饰器是我个人觉得比函数更好的方式，其原因之一是类可以提供更好的封装（相对于python中的函数而言），同时可以在类中编写其他的功能以扩展这个装饰器。
我经常使用如下装饰器，它的功能是作为一个注册器，把所有需要的对象都通过符号表注册到一起，这样方便搜索和调用。
```python3
from functools import wraps

class ViewRegister(object):
	def __init__(self):
		self.view_storage = dict()

	def search(view_name):
		return self.view_storage.get(view_name, None)

	def __call__(self, view_name):
		def outer(view_func):
			@wraps(view_func)
			def inner(*args, **kwargs):
				return view_func(*args, **kwargs)
			return inner
		return outer

register = ViewRegister()

@register('login')
def login(request):
	pass

@register('account')
def account(request):
	pass

@register('article')
def article(request):
	pass

for view_name, view_func in register.view_storage.items():
	print(view_name, view_func)

# 结果是:
# login <function login_view at 0x00000175ADBFAEA0>
# account <function show_account_view at 0x00000175ADBFAF28>
# article <function show_article_view at 0x00000175ADC15048>
```