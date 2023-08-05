/*有5个同学，每个学生的数据包括学号，姓名，3门课程成绩，
从键盘输入5个学生成绩，
要求输出3门课程总平均成绩，
以及最高分的学生的数据(包括学号、姓名、3门课程成绩、平均成绩)。
要求定义结构体变量实现。
*/
#include<stdio.h>
#define N 5
typedef struct
{
    int num; 
    char name[10];
    double score1,score2,score3,equal;
}STU;
int main()
{
    STU stu[N]={{0,{'\0'}}},*p_stu=&stu[0];
    int i;
    for(i=0;i<N;i++)
    {
        printf("Please enter the school number of the %d student:\n",i+1);
        scanf("%d",&stu[i].num);
        printf("Please enter the name of the %d student:\n",i+1);
        scanf("%s",stu[i].name);
        printf("Please enter three scores of the %d student:\n",i+1);
        scanf("%lf%lf%lf",&stu[i].score1,&stu[i].score2,&stu[i].score3);
        stu[i].equal=(stu[i].score1+stu[i].score2+stu[i].score3)/3;
        if(stu[i].equal>p_stu->equal)p_stu=&stu[i];//令结构体指针指向平均成绩最高的学生所对应的结构体
    }
    printf("The data of the student who have got the highest score:\nstudent number:%d\nname:%s\nthe score of each subject:%.2lf %.2lf %.2lf\nthe equal scpre:%.3lf\n",p_stu->num,p_stu->name,p_stu->score1,p_stu->score2,p_stu->score3,p_stu->equal);
    return 0;
}