# 3-1 基础单链表操作

# 题目描述

请完成单链表的基础操作，包括链表尾部插入，链表第k个位置后插入，删除第k个元素，查询第k个元素等操作。

## 备注:

链表表尾部插入，当链表为空时创建一个结点。

链表第k个位置后插入，k=0表示插入元素作为新的头结点。

删除第k个元素，当链表为空时头结点设为空指针。

结点结构体：

```
struct Node{

Node* next;

int value;

Node(int val):value(val),next(nullptr){}

};
```



需要完成的函数：

```
Node* List::SearchkthNode(int k);

void List::InsertBack(Node* n);

void List::DeleteElement(int k);

void List::InsertAfterKth(Node* n, int k);
```

需要添加到List.cpp的依赖文件：`Lish.h`


