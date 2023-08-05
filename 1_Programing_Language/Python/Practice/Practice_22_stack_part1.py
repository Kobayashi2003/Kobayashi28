class Stack:

    """this is a class of Stack"""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def push_lsit(self, l):
        self.items += l

    def pop(self):
        return self.items.pop()

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def top(self):
        return self.items[-1]

    def print_stack(self):
        for item in self.items:
            print(item, end=' ')

    def clear(self):
        self.items.clear()
