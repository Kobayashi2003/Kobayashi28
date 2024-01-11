#include <iostream>
#include <vector>
#define exit
#include "answer.h"

std::vector<int> temp;

bool test(ListNode *list, const std::vector<int> &ans)
{
    temp.clear();
    while (list)
    {
        temp.push_back(list->val);
        list = list->next;
    }
    return ans == temp;
}

int main()
{
    auto list1 = new ListNode(1), test1 = list1;
    list1->next = new ListNode(2);
    list1 = list1->next;
    list1->next = new ListNode(3);
    list1 = list1->next;
    list1->next = new ListNode(4);
    list1 = list1->next;
    list1->next = new ListNode(5);

    auto res1 = reverseKGroup(test1, 3);
    std::cout << test(res1, {3, 2, 1, 4, 5}) << (allNodes <= 6);

    auto list2 = new ListNode(1), test2 = list2;
    list2->next = new ListNode(2);
    list2 = list2->next;
    list2->next = new ListNode(3);
    list2 = list2->next;
    list2->next = new ListNode(4);
    list2 = list2->next;
    list2->next = new ListNode(5);

    auto res2 = reverseKGroup(test2, 1);
    std::cout << test(res2, {1, 2, 3, 4, 5}) << (allNodes <= 12);

    auto list3 = new ListNode(1);
    auto res3 = reverseKGroup(list3, 1);
    std::cout << test(res3, {1}) << (allNodes <= 14);

    auto list4 = new ListNode(1), test4 = list4;
    list4->next = new ListNode(2);
    list4 = list4->next;
    list4->next = new ListNode(3);
    list4 = list4->next;
    list4->next = new ListNode(4);
    list4 = list4->next;
    list4->next = new ListNode(5);
    list4 = list4->next;
    list4->next = new ListNode(6);
    list4 = list4->next;
    list4->next = new ListNode(7);
    list4 = list4->next;
    list4->next = new ListNode(8);
    list4 = list4->next;
    list4->next = new ListNode(9);
    list4 = list4->next;

    auto res4 = reverseKGroup(test4, 4);
    std::cout << test(res4, {4, 3, 2, 1, 8, 7, 6, 5, 9}) << (allNodes <= 24);
}
