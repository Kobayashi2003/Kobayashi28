#include <stdlib.h> 
struct Node {
	struct Node* next;
	int value;
};

void insert(struct Node** head, int num);

void print_linklist(struct Node* head);

void delete_linklist(struct Node* head);

void insert(struct Node** head, int num) {
    struct Node* cur = *head;
    struct Node* prev = NULL;
    while (cur != NULL && cur->value < num) {
        prev = cur;
        cur = cur->next;
    }

    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));
    new_node->value = num;
    new_node->next = cur;
    if (prev == NULL) {
        *head = new_node;
    } else {
        prev->next = new_node;
    }
}

void print_linklist(struct Node* head) {
    struct Node* cur = head;
    while (cur != NULL) {
        printf("%d ", cur->value);
        cur = cur->next;
    }
}

void delete_linklist(struct Node* head) {
    struct Node* cur = head;
    while (cur != NULL) {
        struct Node* temp = cur;
        cur = cur->next;
        free(temp);
    }
}