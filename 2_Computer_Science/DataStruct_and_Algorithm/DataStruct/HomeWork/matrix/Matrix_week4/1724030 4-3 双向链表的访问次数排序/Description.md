# 4-3 双向链表的访问次数排序

# 题目描述

有一个双向链表，链表中节点的定义如下：

```
struct Node{
    Node* prior;
    Node* next;
    int value;
    int freq;
    Node(int val, int fre):value(val),freq(fre),prior(nullptr),next(nullptr){}
};
```

prior指向前驱节点，next指向后继节点，data为储存的数值，freq为对该节点的访问次数，每次通过`Locate(Node* head, int x)`访问该链表时，data值为x的节点的freq增加1。

你需要实现下述函数，使得访问节点后更改其freq值并调整节点位置，使双向链表继续按照freq降序排列。

```
Node* Locate(Node* head, int x);
```

# 样例

双向链表如下图所示，所有节点根据freq的值降序排列，首节点为head。此时，通过Locate(head, 6)访问data值为6的节点。

![1.png](/api/users/image?path=4523/images/1662805683132.png)

访问data为6的节点，其freq增加1，变为2，超过了前一个节点的freq，故交换二者位置。

![2.png](/api/users/image?path=4523/images/1662805881509.png)

# 注意


1. 链表中的节点data值不重复；
2. `Locate`函数返回freq最大的节点指针，即经过调整后的head；
3. 需要添加到`function.cpp`的依赖文件：`function.h`




