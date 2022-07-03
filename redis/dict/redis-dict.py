# -*- coding: utf-8 -*-

"""
redis hash实现，支持渐进式和一次性哈希，使用数组+冲突链表。
"""

from typing import (
    List,
    Union,
)


# 全局数据
class NotFound(object):
    pass


NOT_FOUND = NotFound()
DICTIONARY_INITIAL_SIZE = 4
NOT_AT_REHASH = -1
PROGRESSIVE_REHASH_THRESHOLD = 10
PROGRESSIVE_REHASH_INITIAL_INDEX = 0
HASHMAP_LOAD_OVERFLOW_THRESHOLD = 1
HASHMAP_LOAD_SHORTAGE_THRESHOLD = 0.25


class Entry(object):
    def __init__(self, key: str, value: any, next: "Entry" = None):
        self.key = key
        self.value = value
        self.next = next

    def to_list(self) -> List["Entry"]:
        if self.next is None:
            return [self]
        else:
            return [self] + self.next.to_list()

    def has(self, k: str) -> bool:
        if self.key == k:
            return True
        else:
            if self.next is None:
                return False
            else:
                return self.next.has(k)

    def get(self, k: str) -> Union[NotFound, any]:
        if self.key == k:
            return self.value
        else:
            if self.next is None:
                return NOT_FOUND
            else:
                return self.next.get(k)

    def set(self, k: str, v: any) -> bool:
        if self.key == k:
            self.value = v
            return False
        else:
            if self.next is None:
                new_entry = Entry(k, v)
                self.next = new_entry
                return True
            else:
                return self.next.set(k, v)

    def delete(self, k: str) -> Union["Entry", None]:
        if self.key == k:
            return self.next
        else:
            if self.next is None:
                return self
            else:
                self.next = self.next.delete(k)
                return self

    def __str__(self):
        if self.next is None:
            return '%s:%s' % (self.key, self.value)
        else:
            return '%s:%s' % (self.key, self.value) + ' -> ' + str(self.next)

    __repr__ = __str__


class HashMap(object):
    def __init__(self, initial_size: int):
        self.storage: List[Union[Entry, None]] = [None] * initial_size
        self.size = initial_size
        self.used = 0

    @property
    def storage_length(self) -> int:
        return len(self.storage)

    @property
    def load(self) -> float:
        res = self.used / self.size
        return res

    @property
    def load_overflow(self) -> bool:
        return self.load > HASHMAP_LOAD_OVERFLOW_THRESHOLD

    @property
    def load_shortage(self) -> bool:
        if self.size <= DICTIONARY_INITIAL_SIZE:
            return False
        else:
            return self.load < HASHMAP_LOAD_SHORTAGE_THRESHOLD

    @property
    def entries(self) -> List[Entry]:
        total = []

        for entry in self.storage:
            if isinstance(entry, Entry):
                total.extend(entry.to_list())
            else:
                pass

        return total

    def rebuild_storage(self, new_size: int) -> None:
        """重建数组"""

        self.storage = [None] * new_size
        self.size = new_size
        self.used = 0
        return None

    def list_by_index(self, index: int) -> List[Entry]:
        entry = self.storage[index]

        if isinstance(entry, Entry):
            return entry.to_list()
        else:
            return []

    def clear(self) -> None:
        self.storage = []
        self.size = 0
        self.used = 0
        return None

    def has(self, k: str) -> bool:
        index = self.cal_hash(k)
        entry = self.storage[index]

        if isinstance(entry, Entry):
            return entry.has(k)
        else:
            return False

    def get(self, k: str) -> Union[NotFound, any]:
        index = self.cal_hash(k)
        entry = self.storage[index]

        if isinstance(entry, Entry):
            return entry.get(k)
        else:
            return NOT_FOUND

    def set(self, k: str, v: any) -> None:
        index = self.cal_hash(k)
        entry = self.storage[index]

        if isinstance(entry, Entry):
            res = entry.set(k, v)

            if res:
                self.used += 1
                return None
            else:
                return None
        else:
            new_entry = Entry(k, v)
            self.storage[index] = new_entry
            self.used += 1
            return None

    def delete(self, k: str) -> bool:
        index = self.cal_hash(k)
        entry = self.storage[index]

        if isinstance(entry, Entry):
            if entry.has(k):
                res = entry.delete(k)
                self.used -= 1
                self.storage[index] = res
                return True
            else:
                return False
        else:
            return False

    def cal_hash(self, k: str) -> int:
        index = hash(k) % self.size
        return index

    def rehash_complete(self, new_size: int) -> None:
        new_hashmap = HashMap(new_size)

        for entry in self.entries:
            new_hashmap.set(entry.key, entry.value)

        self.storage = new_hashmap.storage
        self.size = new_hashmap.size
        self.used = new_hashmap.used

        return None


class Dictionary(object):
    def __init__(self, initial_size: int = DICTIONARY_INITIAL_SIZE):
        self.h = [
            HashMap(initial_size),
            HashMap(0),
        ]
        self.rehashid = NOT_AT_REHASH
        print('初始化字典，大小: %s, rehashid: %s' % (initial_size, self.rehashid))

    @property
    def h0(self) -> HashMap:
        return self.h[0]

    @property
    def h1(self) -> HashMap:
        return self.h[1]

    @property
    def is_during_rehash(self) -> bool:
        """是否处于渐进式rehash流程中"""

        res = self.rehashid != NOT_AT_REHASH
        if res:
            print('处于渐进式rehash流程中')
            return res
        else:
            return res

    # 用户界面
    def get(self, k: str) -> Union[NotFound, any]:
        if self.is_during_rehash:
            h1_v = self.h1.get(k)

            if h1_v is NOT_FOUND:
                h0_v = self.h0.get(k)

                if h0_v is NOT_FOUND:
                    res = h0_v
                else:
                    self.h1.set(k, h0_v)
                    res = h0_v
            else:
                res = h1_v

            self.rehash_progressive()
            return res
        else:
            return self.h0.get(k)

    def set(self, k: str, v: any) -> None:
        if self.is_during_rehash:
            if self.h0.has(k):
                self.h0.set(k, v)
                self.h1.set(k, v)
            else:
                self.h1.set(k, v)

            self.rehash_progressive()
            return None
        else:
            self.h0.set(k, v)

            if self.h0.load_overflow:
                print('h0负载溢出: %s' % self.h0.load)
                self.do_rehash(1)
                return None
            else:
                return None

    def delete(self, k: str) -> bool:
        if self.is_during_rehash:
            h1_res = self.h1.delete(k)
            h0_res = self.h0.delete(k)
            return h1_res or h0_res
        else:
            d_res = self.h0.delete(k)

            if d_res is True and self.h0.load_shortage:
                print('h0负载短缺: %s' % self.h0.load)
                self.do_rehash(-1)
                return d_res
            else:
                return d_res

    def do_rehash(self, d: int) -> None:
        """
        触发字典的rehash逻辑。
        1 是扩容
        -1 是缩容
        如果h0使用量小于一定阈值，则执行完整hash策略，否则，执行渐进式hash策略。
        """

        assert self.rehashid == NOT_AT_REHASH

        if self.h0.used < PROGRESSIVE_REHASH_THRESHOLD:
            print('触发完整rehash策略')
            self.rehash_complete(self.h0, d)
            return None
        else:
            print('触发渐进式rehash策略，h0 used: %s' % self.h0.used)
            self.declare_during_rehash(d)
            self.rehash_progressive()
            return None

    def rehash_complete(self, h: HashMap, d: int) -> None:
        """
        执行完整rehash流程
        """

        if d == 1:
            h.rehash_complete(h.size * 2)
        else:
            h.rehash_complete(h.size // 2)

        return None

    def declare_during_rehash(self, d: int) -> None:
        """
        声明进入渐进式rehash流程
        """

        if d == 1:
            self.h1.rebuild_storage(self.h0.size * 2)
        else:
            self.h1.rebuild_storage(self.h0.size // 2)

        self.rehashid = PROGRESSIVE_REHASH_INITIAL_INDEX
        print('声明进入渐进式rehash流程，rehashid: %s, h1 size: %s' % (self.rehashid, self.h1.size))
        return None

    def rehash_progressive(self) -> None:
        """
        执行渐进式rehash流程
        """

        print('执行渐进式rehash流程')
        assert self.rehashid < self.h0.storage_length

        entries = self.h0.list_by_index(self.rehashid)
        for entry in entries:
            self.h1.set(entry.key, entry.value)
        self.rehashid += 1

        if self.rehashid >= self.h0.storage_length:
            self.declare_finish_rehash()
            self.h0.clear()
            self.h[0], self.h[1] = self.h[1], self.h[0]
            print('当前是最后一次渐进式rehash流程')
            return None
        else:
            return None

    def declare_finish_rehash(self) -> None:
        """
        声明完成渐进式rehash流程
        """

        self.rehashid = NOT_AT_REHASH
        print('声明完成渐进式rehash流程, rehashid: %s' % self.rehashid)
        return None


d1 = Dictionary()
d1.set('a', 2)
d1.set('b', 2)
d1.set('c', 2)
d1.set('d', 2)
d1.set('h', 2)
d1.set('i', 2)
d1.set('j', 2)
d1.set('k', 2)
d1.set('l', 2)
d1.set('m', 2)
d1.set('n', 2)
d1.set('o', 2)
d1.set('p', 2)
d1.set('r', 2)
d1.set('s', 2)
d1.set('t', 2)
d1.set('u', 2)
d1.set('v', 2)
