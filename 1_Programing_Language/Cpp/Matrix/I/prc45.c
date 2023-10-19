#include <stdio.h>
#include<stdlib.h>

typedef struct Staff{
    int id;
    int age;
    int wages;
    char name[11];
    struct Staff *next;
}staff;
void insertStaff(staff *head);
void deleteStaff(staff *head,int id);
int getTotalStaff(staff *head);
int getAvgWages(staff *head);
int getMaxAge(staff *head);

void insertStaff(staff *head){
    staff *p = head;
    while(p->next!=NULL){
        p = p->next;
    }
    staff *newStaff = (staff *)malloc(sizeof(staff));
    scanf("%d %d %d %s",&newStaff->id,&newStaff->age,&newStaff->wages,newStaff->name);
    newStaff->next = NULL;
    p->next = newStaff;
}

void deleteStaff(staff *head,int id){
    staff *p = head;
    while(p->next!=NULL){
        if(p->next->id==id){
            staff *q = p->next;
            p->next = q->next;
            free(q);
            return;
        }
        p = p->next;
    }
}

int getTotalStaff(staff *head){
    int count = 0;
    staff *p = head->next;
    while(p!=NULL){
        count++;
        p = p->next;
    }
    return count;
}

int getAvgWages(staff *head){
    int count = 0;
    int sum = 0;
    staff *p = head->next;
    while(p!=NULL){
        count++;
        sum+=p->wages;
        p = p->next;
    }
    if (count==0) return 0;
    return sum/count;
}

int getMaxAge(staff *head){
    int maxAge = 0;
    staff *p = head->next;
    while(p!=NULL){
        if(p->age>maxAge){
            maxAge = p->age;
        }
        p = p->next;
    }
    return maxAge;
}


int main()
{

    // 输入n代表有n条指令(0<n<=100)
    // 接下来有n条指令的相关操作 order（1<=order<=5）,当order为1或2时会有额外的录入，具体如下：
    // order 为1：输入员工信息（员工id（保证id不重复），员工年龄，员工工资，员工姓名（姓名长度不超过10））。
    // order 为2：输入id号

    int orderCount;
    int id;
    scanf("%d",&orderCount);
    staff *head = (staff *)malloc(sizeof(staff)),*p,*q;
    head->next = NULL;
    //输入基本员工树
    while(orderCount--){
        int order;
        scanf("%d",&order);
        switch(order){
        case 1:
            //录入员工
            insertStaff(head);
            printf("员工总数：%d\n",getTotalStaff(head));
            break;
        case 2:
            scanf("%d",&id);
            //删除员工
            deleteStaff(head,id);
            printf("员工总数：%d\n",getTotalStaff(head));
            break;
        case 3:
            //最高年龄
            printf("员工最高年龄：%d\n",getMaxAge(head));
            break;
        case 4:
            //平均薪资,
            printf("员工平均薪资：%d\n",getAvgWages(head));
            break;
        case 5:
            //员工总数
            printf("员工总数：%d\n",getTotalStaff(head));
        }
    }
    p = head->next;
    while(p!=NULL){
        q = p;
        p = p->next;
        free(q);
    }
    if(head!=NULL) free(head);
    return 0;
}
