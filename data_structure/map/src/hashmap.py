# -*- coding: utf-8 -*-

"""
hashmap的python实现。

1. 支持增删改查。
2. 使用简易模运算模拟hash函数。
3. 冲突处理使用冲突链表。
4. key要求为str，value是any。key的类型仅str不是重点。
5. 支持负载因子，动态扩容和缩容。
6. 不考虑线程安全问题。

"""

from decimal import Decimal

from typing import (
    Tuple,
    List,
    Union,
)


class Item(object):
    def __init__(self, key: str, value: any):
        self.key = key
        self.value = value

    def check_key(self, k: str) -> Union[AssertionError, None]:
        if k == self.key:
            return None
        else:
            raise AssertionError(
                '当前key: %s 与 已存在的 key: %s 哈希到了同一个位置，不可能'
                % (k, self.key)
            )

    def update_value(self, new_value: any) -> None:
        self.value = new_value
        return None

    def __str__(self):
        return '(Item %s %s)' % (
            self.key,
            self.value
        )

    __repr__ = __str__


class Node(object):
    def __init__(self, key: str, value: any, next=None):
        self.key = key
        self.value = value
        self.next = next

    @property
    def items(self) -> List[Tuple[str, any]]:
        if self.next is None:
            return [(self.key, self.value)]
        else:
            current_item = [(self.key, self.value)]
            current_item.extend(self.next.items)
            return current_item

    def set_key_value(self, k: str, v: any) -> Union[None, str]:
        """更新的话返回None，增加的话返回key"""

        if k == self.key:
            self.value = v
            return None
        else:
            if self.next is not None:
                return self.next.set_key_value(k, v)
            else:
                new_node = Node(k, v)
                self.next = new_node
                return k

    def get_key_value(self, k: str, default: any = None) -> any:
        if k == self.key:
            return self.value
        else:
            if self.next is not None:
                return self.next.get_key_value(k, default)
            else:
                if default:
                    return default
                else:
                    raise KeyError('自定义哈希表中没有找到这个key: %s' % k)

    def delete_key_value(self, k: str):
        """
        如果删head，返回next
        如果是最后一个节点，返回None
        如果没找到，raise KeyError
        """

        if k == self.key:
            return self.next
        else:
            if self.next is not None:
                self.next = self.next.delete_key_value(k)
                return self
            else:
                raise KeyError('自定义哈希表中没有找到这个key: %s' % k)

    def __str__(self):
        if self.next is None:
            return '(Node %s %s)' % (self.key, self.value)
        else:
            next_node_repr = str(self.next)
            cur_node_repr = '(Node %s %s)' % (self.key, self.value)
            final_repr = cur_node_repr + ' -> ' + next_node_repr
            return final_repr

    __repr__ = __str__


class StorageManager(object):
    MIN_LENGTH = 10

    def __init__(self, initial_length: int = MIN_LENGTH):
        self.length = initial_length
        self._storage = self.initial_storage()
        self._load = 0
        self._max_load_rate = Decimal('0.75')
        self._min_load_rate = Decimal('0.2')

    @property
    def load_rate(self) -> Decimal:
        return Decimal(self._load / self.length)

    @property
    def is_load_overflow(self) -> bool:
        return self.load_rate > self._max_load_rate

    @property
    def is_load_small(self) -> bool:
        return self.load_rate < self._min_load_rate

    @property
    def items(self) -> List[Tuple[str, any]]:
        res = []

        for slot in self._storage:
            if slot is None:
                pass
            elif isinstance(slot, Item):
                res.append((slot.key, slot.value))
            elif isinstance(slot, Node):
                res.extend(slot.items)
            else:
                raise AssertionError('不可能的类型: %s' % slot.__class__)

        return res

    def increase_load(self):
        self._load += 1
        print('current load rate: %.2f' % self.load_rate)
        return None

    def decrease_load(self):
        self._load -= 1
        print('current load rate: %.2f' % self.load_rate)
        return None

    def try_resize(self) -> None:
        if self.is_load_overflow:
            print('load overflow')
            new_length = self.length * 2
        elif self.is_load_small:
            if self.length == self.MIN_LENGTH:
                return None
            else:
                print('load small')
                temp_length = self.length // 2
                new_length = max(self.MIN_LENGTH, temp_length)
        else:
            return None

        # 把当前的数据都映射过去
        new_manager = StorageManager(new_length)
        print('new manager: %s' % str(StorageManager))

        for key, value in self.items:
            new_manager.set_storage(key, value)
            new_manager.increase_load()

        self.length = new_manager.length
        self._storage = new_manager._storage
        self._load = new_manager._load
        return None

    def initial_storage(self) -> List:
        return [None] * self.length

    def key_to_index(self, key: str) -> int:
        index = int(str(id(key))[-5:]) % self.length
        return index

    def set_storage(self, key: str, value: any) -> Union[None, str]:
        """
        更新的话返回None，增加的话返回key
        """

        index = self.key_to_index(key)
        exist_thing = self._storage[index]

        if exist_thing is None:
            self._storage[index] = Item(key, value)
            return key
        elif isinstance(exist_thing, Item):
            if exist_thing.key == key:
                exist_thing.update_value(value)
                return None
            else:
                old_node = Node(exist_thing.key, exist_thing.value)
                new_node = Node(key, value)
                old_node.next = new_node
                self._storage[index] = old_node
                return key
        elif isinstance(exist_thing, Node):
            return exist_thing.set_key_value(key, value)
        else:
            raise AssertionError('不可能的类型: %s' % exist_thing.__class__)

    def get_storage(self, key: str, default: any = None) -> any:
        index = self.key_to_index(key)
        exist_thing = self._storage[index]

        if exist_thing is None:
            if default:
                return default
            else:
                raise KeyError('自定义哈希表中没有找到这个key: %s' % key)
        elif isinstance(exist_thing, Item):
            exist_thing.check_key(key)
            return exist_thing.value
        elif isinstance(exist_thing, Node):
            return exist_thing.get_key_value(key, default)
        else:
            raise AssertionError('不可能的类型: %s' % exist_thing.__class__)

    def delete_storage(self, key: str) -> Union[None, KeyError]:
        index = self.key_to_index(key)
        exist_thing = self._storage[index]

        if exist_thing is None:
            raise KeyError('自定义哈希表中没有找到这个key: %s' % key)
        elif isinstance(exist_thing, Item):
            if exist_thing.key == key:
                self._storage[index] = None
            else:
                raise KeyError('自定义哈希表中没有找到这个key: %s' % key)
            return None
        elif isinstance(exist_thing, Node):
            new_head = exist_thing.delete_key_value(key)
            self._storage[index] = new_head
            return None
        else:
            raise AssertionError('不可能的类型: %s' % exist_thing.__class__)


class Directory(object):
    def __init__(self):
        self.storage_manager = StorageManager()

    def __setitem__(self, key, value):
        return self.hash_set(key, value)

    def __getitem__(self, item):
        return self.hash_get(item)

    def __delitem__(self, key):
        return self.hash_delete(key)

    @property
    def items(self) -> List[Tuple[str, any]]:
        return self.storage_manager.items

    @property
    def keys(self) -> List[str]:
        return list(map(lambda item: item[0], self.items))

    @property
    def values(self) -> List[str]:
        return list(map(lambda item: item[1], self.items))

    def hash_get(self, key: str, default: any = None) -> any:
        """
        等价于 d[key]
        """

        value = self.storage_manager.get_storage(key, default)
        return value

    def hash_set(self, key: str, value: any) -> None:
        """
        等价于 d[key] = value
        """

        k = self.storage_manager.set_storage(key, value)

        if k:
            self.storage_manager.increase_load()
            self.storage_manager.try_resize()
            return None
        else:
            return None

    def hash_delete(self, key: str) -> Union[None, KeyError]:
        """
        等价于 del d[key]
        """

        self.storage_manager.delete_storage(key)
        self.storage_manager.decrease_load()
        self.storage_manager.try_resize()
        return None


d1 = Directory()

# 测试
d1['yc'] = 1
d1['ly'] = 2
d1['wz'] = 3
d1['wl'] = 4
d1['zx'] = 5
d1['ab'] = 6
