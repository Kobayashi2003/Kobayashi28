#include<stdio.h>
#include<string.h>
int main()
{
    struct Student
    {
        long num;
        char name[20];
        char sex;
        float score;
    };
    struct Student stu_1;
    struct Student *p;
    p=&stu_1;
    stu_1.num=10101;
    strcpy(stu_1.name,"Li Lin");
    stu_1.sex='M';;
    stu_1.score=89.5;
    printf("No :%ld\nname:%s\nsex:%c\nscore:%5.1f\n",(*p).num,(*p).name,(*p).sex,(*p).score);
    return 0;
}