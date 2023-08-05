// 将两个升序列表连接成一个升序列表并返回

#include<stdio.h>
#include<stdlib.h>

#define N 10000

#define LEN (sizeof(Node))

typedef struct Node {
    int val;
    struct Node *next;
}Node;

void init(Node *node, int val) {
    node -> val = val;
    node -> next = NULL;
}

void createList(Node *head, int num[], int len) {
    Node *oldNode = head;
    for (int i = 0; i < len; i++) {
        Node *newNode = (Node*)malloc(LEN);
        init(newNode, num[i]);
        oldNode -> next = newNode;
        oldNode = newNode;
    }
}

void showList(Node *head) {
    Node *p = head -> next;
    while(p !=NULL) {
        // printf("%d\n", p->val);
        printf("%d ", p->val);
        p = p -> next;
    }
}

Node * connect(Node *head1, Node *head2) {
    if (head2 -> next == NULL) {
        return head1;
    } else if (head2 -> next == NULL) {
        return head2;
    }
    Node * head = (Node*)malloc(LEN);
    init(head, 0);
    Node *p1 = head1 -> next;
    Node *p2 = head2 -> next;
    Node * tail = head;
    while(p1 && p2) {
        if (p1 -> val < p2 -> val) {
            tail -> next = p1;
            p1 = p1 -> next;
        } else {
            tail -> next = p2;
            p2 = p2 -> next;
        }
        tail = tail -> next;
    }
    if (p1 == NULL) {
        tail -> next = p2;
    } else {
        tail -> next = p1;
    }
    return head;
}

int main() {
    Node * head1 = (Node*)malloc(LEN);
    Node * head2 = (Node*)malloc(LEN);
    init(head1, 0);
    init(head2, 0);
    // int num1[] = {1, 2, 4, 9};
    // int num2[] = {1, 3, 4};
    int n1, n2;
    scanf("%d%d", &n1, &n2);
    int num1[N] = {0};
    int num2[N] = {0};
    for (int i = 0; i < n1; ++i) {
        scanf("%d", &num1[i]);
    }
    for (int i = 0; i < n2; ++i) {
        scanf("%d",&num2[i]);
    }
    // createList(head1, num1, (sizeof(num1)/sizeof(int)));
    // createList(head2, num2, (sizeof(num2)/sizeof(int)));
    createList(head1, num1, n1);
    createList(head2, num2, n2);
    Node *head = connect(head1, head2);
    showList(head);
    return 0;
}