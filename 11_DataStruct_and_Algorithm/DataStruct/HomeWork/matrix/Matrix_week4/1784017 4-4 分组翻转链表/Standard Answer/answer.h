#include "ListNode.h"
#include <utility>
// 翻转一个子链表，并且返回新的头与尾
std::pair<ListNode *, ListNode *> myReverse(ListNode *head, ListNode *tail)
{
    ListNode *prev = tail->next;
    ListNode *p = head;
    while (prev != tail)
    {
        ListNode *nex = p->next;
        p->next = prev;
        prev = p;
        p = nex;
    }
    return {tail, head};
}

ListNode *reverseKGroup(ListNode *head, int k)
{
    ListNode *hair = new ListNode(0);
    hair->next = head;
    ListNode *pre = hair;

    while (head)
    {
        ListNode *tail = pre;
        // 查看剩余部分长度是否大于等于 k
        for (int i = 0; i < k; ++i)
        {
            tail = tail->next;
            if (!tail)
            {
                return hair->next;
            }
        }
        ListNode *nex = tail->next;

        auto result = myReverse(head, tail);
        head = result.first;
        tail = result.second;

        // 把子链表重新接回原链表
        pre->next = head;
        tail->next = nex;
        pre = tail;
        head = tail->next;
    }

    return hair->next;
}
