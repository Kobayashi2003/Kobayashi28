struct ListNode
{
    int value;
    struct ListNode *next;
};

struct ListNode* ReverseList(struct ListNode *head);

struct ListNode* ReverseList(struct ListNode *head)
{
    struct ListNode *p, *q, *r;
    p = head;
    q = NULL;
    while (p != NULL)
    {
        r = q;
        q = p;
        p = p->next;
        q->next = r;
    }
    return q;
}