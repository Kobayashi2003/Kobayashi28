# 3-3 逆序合并有序单链表

# 题目描述

给定2个升序排列的有序单链表，将其合并成一个有序单链表，并进行逆序操作。

输入：2个单链表的数据。

输出：合并逆序后的单链表。

结构体：

```
struct Node{
    Node* next;
    int value;
    Node(int val):value(val),next(nullptr){}
};
```



## 样例输入

```
2 5 6 8 9
1 3 4 7
```

## 样例输出

`9 8 7 6 5 4 3 2 1`

## 要求完成函数：

```
Node* ReverseMergeList(Node* List1, Node* List2);
```

需要在function.cpp添加的头文件：`function.h`

