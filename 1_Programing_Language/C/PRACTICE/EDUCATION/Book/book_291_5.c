#include<stdio.h>
#define N 5
#define mark 1
#define Ture 1
#define False 0
int LastPerson(int *person)
{
    int count=0,flag;//count用于记数没有被淘汰的人
    for(int i=0;i<N;i++)
        if(person[i]==0)
        {
            count++;
            flag=i;//flag用于标记最后一位没有被淘汰的人
        }
    if(count==1)//当只剩下最后一人时，调用flag将其序号输出
    {
        printf("The %d person is the last person\n",flag+1);
        return Ture;
    }
    return False;
}

int Judge(int num)//用于判断num是否为三的倍数
{
    if(num%3)return False;
    return Ture;
}

void Mark(int *person)//标记被淘汰的人
{
    int num=0;
    for(int i=0;LastPerson(person)^1;i=(i+1)%N)
    {
        while(person[i])i=(i+1)%N;
        if(Judge(++num))person[i]=mark;
    }    
}

int main()
{
    int person[N]={0};
    Mark(person);
    return False;
}


//while(N)