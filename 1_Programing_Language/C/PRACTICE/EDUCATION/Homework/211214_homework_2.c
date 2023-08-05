#include<stdio.h>
#define N 10
#define Mark 0
int main()
{
    void whoIsTheLastOne(int *person,int n);
    int n,person[N]={0};
    int i;
    printf("Please enter the number of the persons:\n");
    scanf("%d",&n);
    for(i=0;i<n;i++)person[i]=i+1;//给每个人进行标号
    whoIsTheLastOne(person,n);
    return 0;
}
void whoIsTheLastOne(int *person,int n)
{
    int num=0,n_temp=n;
    int i;
    for(i=0;n;i=(i+1)%n_temp)
    {
        if(person[i]==Mark)continue;//若当前数为被标记（淘汰）的人，则跳过该次计数
        if(++num%3==0)//若当前数为3的倍数，淘汰并标记此人
        {
            n--;
            if(n==0)printf("The last person is the %d person\n",person[i]);//输出最后一名玩家的编号
            else person[i]=Mark;
        }
    }
}