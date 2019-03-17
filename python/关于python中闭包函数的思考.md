## 基本语言特性
闭包应该作为语言的标准特性，据了解，目前大部分语言使用的都是词法作用域，这就意味着它们都支持闭包。
闭包技术非常有用，尤其是在你需要构造一个私有执行环境的时候。
闭包也是其他技术（如装饰器、生成器）的底层技术支撑。

## 闭包之所以产生的原因是词法作用域
只要编程语言选择的是词法作用域，而不是动态作用域，就可以支持闭包，所以闭包不是python独有的技术。
思考下面这个例子：
```python3
def add(base):
    def inner(num):
        return base + num
    return inner

base = 100
inner_func = add(base)

base = 23
print(inner_func(1))  # 结果是101还是24？
```
我解释一下我对词法作用域的理解。
函数要先被定义，才能被调用。
**当一个函数对象被调用的时候，如果函数的执行环境使用的是此函数定义处的环境，则使用的是词法作用域，即lexcial scope。
当一个函数对象被调用的时候，如果函数的执行环境使用的是调用处的环境，则使用的是动态作用域，即dynamic scope。**
那么到底是使用哪一种执行环境，取决于编程语言的解释器的行为，目前大部分编程语言都选择词法作用域。
当我们使用词法作用域的时候，闭包就产生了。


## 闭包提供了一个执行环境
闭包本质上是一个函数的执行环境，所谓执行环境，其实就是一个符号表，里面包含了变量名与对象地址的映射。
因为闭包的存在，在返回嵌套函数的时候，内层函数总是携带着自己的执行环境，即使我们在最外层去执行内层函数，它依然使用的是自己的（内层）执行环境，这看上去就好像是内层函数一直在保存着数据一样。
所以上面那个例子的结果是101。


## 使用闭包来构造环境以存储数据
闭包的这种特性，在某些场景下非常实用，尤其是在我们需要构造一个环境保存私有数据时，这让我们可以创造一个命名空间。
这是对一颗二叉树执行先序遍历的代码：
```python3
node_list = list()
def recursion(cur_node):
    if cur_node is None:
        return None

    node_list.append(cur_node)
    recursion(cur_node.left)
    recursion(cur_node.right)
```
这样写有几点不足：
- 你的node_list变成了全局变量，换句话说，它被其他函数看到了（这就有被修改或者重名的风险）
- 你无法用一个函数搞定这件事，因为你的存储结构（node_list)和执行逻辑(recursion)分开了，换句话说，你拆开了这两个东西，没有把他们封装到一起（当然你可以用类来封装，但是那样太重了）。

如果是我的话，我会写成这样：
```python3
def show(tree):
    node_list = list()
    def recursion(cur_node):
        if cur_node is None:
            return None

        node_list.append(cur_node)
        recursion(cur_node.left)
        recursion(cur_node.right)
    recursion(tree)
    return node_list
```


其中的递归函数recursion是一个闭包，可以在遍历树的过程中不断的append到外层的node_list上，最后在show函数中return。这样写，对于show函数之外的函数，都看不到node_list结构，这个结构就像是recursion函数“私有的”，同时，执行一个函数就可以得到结果，封装性也提升了。

## 闭包可以用于装饰器模式
当我们理解了闭包的本质和特性之后，理解python的装饰器就非常简单了。
先看看python装饰器使用的代码：
```python3
import time

def show_time(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'函数{func__name__}的执行时间是:', end - start)
        return result
    return inner

@show_time
def add(num):
    time.sleep(1)
    return num + 1
```
装饰器模式有两点前置知识需要理解：
1. 函数可以作为第一类对象传递
2. 闭包

在这个例子中，参数func代表着函数add，此时add函数被作为参数传递，且inner函数作为返回值传递。此时的show_time函数其实是一个高阶函数。

inner函数是一个闭包函数，因为它被嵌套在show_time函数内部并被返回。inner函数有一个闭包环境，里面保存了func函数，所以当inner函数被执行的时候，可以在inner函数的函数体中执行func函数：`result = func(*args, **kwargs)`，这样inner函数的返回值就是func函数的返回值，对业务结果不会有影响。这样看来，show_time函数的作用仅仅是为了返回一个inner闭包函数，而inner闭包函数包裹着func函数，同时增加了一些额外的功能（就是所谓装饰的功能），然后在inner函数内部执行func函数返回正确的业务结果。

## 更多层次的嵌套
如果你理解了双层嵌套函数，那么n层嵌套函数就只是一种推广。
```python3
def outer():
    def mid():
        def inner():
            returnr 23
        return inner
    return mid

print(outer()()())  # 结果是23
```
上面这个例子可以解释python中带参数的装饰器代码。
装饰器的使用后续我会单独写一篇文章。

## 如何访问闭包环境中的数据
闭包函数有一个闭包环境，其实是一个符号表。按理说这个环境是可以被访问到的，python中使用`func.__closure__`来访问闭包函数func的闭包环境。在python中，此环境是只读的。