#include<stdio.h>
#define N 6
void whoIsTheLast(int *person,int n,int flag)
{
    if(n==1)
    {
        printf("%d",person[0]);
        return;
    }
    int person_temp[N]={0};
    for(int num=1;num%3;num++)flag=(flag+1)%n;
    for(int i=0,j=0;i<N;i++,j++)
    {
        if(i==flag)i++;
        person_temp[j]=person[i];
    }
    whoIsTheLast(person_temp,n-1,flag);
}
int main()
{
    int person[N]={0};
    for(int i=0; i<N; i++)person[i]=i+1;
    whoIsTheLast(person,N,0);
    return 0;
}