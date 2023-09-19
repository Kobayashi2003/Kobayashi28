# 1-3 链表的反转

## 题目描述：
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;下面所给的是链表节点的结构，你的任务是写一个函数将链表反转。

```
	struct ListNode {
		int val;
		ListNode *next;
		ListNode(){
			val=0;
			next=NULL;
		}
		ListNode(int x) : val(x), next(NULL) {}
		~ListNode(){}
	};
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;上述结构定义在头文件ListNode.h中，而你所需实现的函数为：
```
ListNode* reverseList(ListNode* head);
```
**提示：**请记得将头文件包含进去，即#include"ListNode.h" 。
## 注意事项：
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;你只需写出reverseList函数实现即可，不用提交main函数。