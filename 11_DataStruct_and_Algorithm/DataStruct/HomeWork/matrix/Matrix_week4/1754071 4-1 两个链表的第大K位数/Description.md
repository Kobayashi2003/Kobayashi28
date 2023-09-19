# 4-1 两个链表的第大K位数

# 题目描述

给定两个单链表，找出其第K大的数。

输入：k表示第k大的数，两个单链表（无重复数字）。

输出：第k大的数的结点。

结构体：

```
struct Node{
    Node* next;
    int value;
    Node(int val):value(val),next(nullptr){}
};
```

## 样例输入：

```
7
7 3 5 9 2
8 1 6 10 4
```

## 样例输出:

```
4
```

## 要求完成的函数：

```
Node* FindKthBigElementInTwoList(Node* List1, Node* List2, int k);
```

需要添加到function.cpp的依赖文件：`function.h`

