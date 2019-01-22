# -*- coding: utf-8 -*-
# 'author': 'zlw'


"""树是一种一对多的关系，所以可以用一个节点来管理多个节点，体现层次关系。
树通常使用链表实现，而链表自身是一维的。
链表增加多个后续节点指针，保持一个前驱节点，就可以在逻辑上形成树。
树这种ADT的元素构成就是链表的节点，包含数据和指针。
树的操作包含了创建、清空，最重要的还有遍历。
树的遍历涵盖非常多的知识点。
树中每一个节点都会被访问3次，根据不同访问时机打印出的遍历结果不同，对应为：前、中、后序。
注意：默认情况下，树的遍历使用递归实现。
而递归的底层是使用栈来实现，所以可以理解成默认的树遍历是通过栈来实现的。
而如果使用队列来实现遍历，则可以实现层序遍历。
不论遍历时的底层使用的是栈还是队列，目的都是为了保存历史访问的树节点，为什么需要保存呢？
因为树的实现是使用单向链表，一旦访问到下一个节点，就无法返回到上一个节点，所以需要使用栈或者队列来保存。
使用不同的结构保存会在输出的时候提现不同的特征。
树的遍历中最核心、最关键的问题就是：如何处理已访问节点的保存问题？如果没有处理好这个问题，就会导致只能遍历一颗子树而无法遍历另一颗。
"""

def show_list(func):
    def wrapper(self):
        self.traverse_list.clear()
        func(self)
        print(self.traverse_list)
    return wrapper


class BinaryTree(object):
    traverse_list = []

    def __init__(self, root_value):
        self.root = root_value
        self.left_child = None
        self.right_child = None
    
    def append_left(self, tree):
        self.left_child = tree

    def append_right(self, tree):
        self.right_child = tree

    @show_list
    def front(self):
        self.traverse_front()

    @show_list
    def mid(self):
        self.traverse_mid()

    @show_list
    def rear(self):
        self.traverse_rear()
    
    @show_list
    def level(self):
        self.traverse_level()

    # 定义前序遍历
    def traverse_front(self):
        self.traverse_list.append(self.root)

        if self.left_child:
            self.left_child.traverse_front()
        if self.right_child:
            self.right_child.traverse_front()

    # 定义中序遍历
    def traverse_mid(self):
        if self.left_child:
            self.left_child.traverse_front()

        self.traverse_list.append(self.root)

        if self.right_child:
            self.right_child.traverse_front()

    # 定义后序遍历
    def traverse_rear(self):
        if self.left_child:
            self.left_child.traverse_front()

        if self.right_child:
            self.right_child.traverse_front()

        self.traverse_list.append(self.root)

    # 定义层序遍历
    def traverse_level(self):
        queue = list()
        queue.append(self)
        while True:
            if not queue:
                break
            tree = queue.pop(0)
            self.traverse_list.append(tree.root)

            if tree.left_child:
                queue.append(tree.left_child)
            if tree.right_child:
                queue.append(tree.right_child)


if __name__ == "__main__":
    pass
    print('hello')
    a = BinaryTree('A')
    b = BinaryTree('B')
    c = BinaryTree('C')
    d = BinaryTree('D')
    e = BinaryTree('E')
    f = BinaryTree('F')
    g = BinaryTree('G')

    # 构建树
    a.append_left(b)
    a.append_right(c)

    b.append_left(d)
    b.append_right(e)

    c.append_left(f)
    c.append_right(g)

    a.front()
    a.mid()
    a.rear()
    a.level()