#include <stdio.h>
#include <stdlib.h>

typedef struct Staff{
    int id;
    int age;
    int wages;
    char name[11];
    struct Staff *next;
}staff;

void registerStaff(int n,staff *head);
void getMaxWages(staff *head);

void registerStaff(int n, staff *head) {
    staff *p = head;
    staff *q;
    for (int i = 0; i < n; ++i) {
        q = (staff*)malloc(sizeof(staff));
        scanf("%d %d %d %s",&q->id,&q->age,&q->wages,q->name);
        q->next = NULL;
        p->next = q;
        p = q;
    }
}

void getMaxWages(staff *head) {
    // find max wages, and change the max to the first
    staff *p = head->next;
    staff *q = head->next;
    staff *max = head->next;
    while(p!=NULL){
        if(p->wages > max->wages){
            max = p;
        }
        p = p->next;
    }
    if(max != q){
        while(q->next != max){
            q = q->next;
        }
        q->next = max->next;
        max->next = head->next;
        head->next = max;
    }
}


int main()
{
    int n;
    staff *head = (staff*)malloc(sizeof(staff));
    head->next = NULL;
    staff *p;
    staff *q;
    scanf("%d",&n);
    registerStaff(n,head);
    getMaxWages(head);
    p = head->next;
    printf("%d\n",p->wages);
    while(p!=NULL){
        printf("%d\n",p->id);
        q = p;
        p = p->next;
        free(q);
    }
    free(head);
    return 0;
}