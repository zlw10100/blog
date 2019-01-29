# 可变长队列
此队列为用户提供容量动态伸缩功能。
用户也可以明确指定容量以固定队列大小。

# 接口定义
**`class RQueue<Item>:`**

* `RQueue(fixed_size=None)`
实例化一个可变长队列对象，默认无需提供`fixed_size`参数。
若提供了此参数，则队列将会固定容量无法伸缩。

* `void enqueue(Item item)`
将一个元素入队，若队列是固长且已满，则抛出`QueueIsFullError`错误。

* `Item dequeue()`
将一个元素出队，不论队列是否固长，只要队列已空，则抛出`QueueIsEmptyError`错误。

* `bool is_empty()`
返回布尔值以判定队列当前是否已空

* `bool is_full()`
返回布尔值以判定队列当前是否已满

* `int size()`
返回整型数值以表明队列当前有效容量

# 迭代
此队列实现了迭代器接口。
