# 4-4 分组翻转链表

## 2-4 分组翻转链表

## 题目描述：

给定一个链表，返回按每k（k<=链表长度）个节点进行翻转的链表
如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序

```
struct ListNode
{
    int val = 0;
    ListNode *next = nullptr;
    ListNode(int x = 0) : val(x) {}
};
```

实现函数

```
ListNode* reverseKGroup(ListNode* head, int k);
```

示例：
已知链表： *1,2,3,4,5 *  *k = 2*
返回：     *2,1,4,3,5*
**提示*** 请记得将头文件包含进去，即`#include"ListNode.h"`，链表的节点从1开始计数

* 传入与返回链表无头节点
* 你可以至多new 1个头节点
* `allNodes`仅测试用，不代表链表长度，请不要使用

