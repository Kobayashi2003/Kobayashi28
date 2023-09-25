/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x , ListNode *next) : val(x), next(next) {}
};


class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        bool carry = false;
        ListNode *head = new ListNode();
        ListNode *p = head;
        while (l1 != nullptr && l2 != nullptr) {
            short sum = l1->val + l2->val + carry;
            carry = sum / 10;
            p->next = new ListNode(sum % 10);
            p = p->next; 
            l1 = l1->next; l2 = l2->next;
        }
        ListNode *rest = l1 == nullptr ? l2 : l1;
        while (rest != nullptr) {
            short sum = rest->val + carry;
            carry = sum / 10;
            p->next = new ListNode(sum % 10);
            p = p->next;
            rest = rest->next;
        }

        if (carry) {
            p->next = new ListNode(1);
        }

        return head->next;
    }
};