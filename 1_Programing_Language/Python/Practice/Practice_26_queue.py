# 用 Python 实现队列
# 队列主要特性：数据先进先出
# 需求：实现 入队，出队，判空，获取队列大小和队头元素 这几项基本功能

class Queue:

    def __init__(self):
        items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def top(self):
        return self.items[0]