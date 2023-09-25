# test the class Stack

from 220916_stack_part1 import Stack

stack = Stack()
print(stack.isEmpty())
stack.push(0)
stack.push_lsit(list(range(1, 10)))
print(stack.size())
print(stack.top())
print(stack.pop())
stack.print_stack()