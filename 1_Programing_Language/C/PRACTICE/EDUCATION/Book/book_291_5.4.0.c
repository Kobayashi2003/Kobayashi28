#include<stdio.h>
#define N 10
#define Mark 0
void whoIsTheLastOne(int *person,int n)
{
    int num=0,n_temp=n;
    int i;
    for(i=0;n;i=(i+1)%n_temp)
    {
        if(person[i]==Mark)continue;
        if(++num%3==0)
        {
            n--;
            if(n==0)printf("The last person is the %d person\n",person[i]);
            else person[i]=Mark;
        }
    }
}
int main()
{
    int n,person[N]={0};
    int i;
    printf("Please enter the number of the persons:\n");
    scanf("%d",&n);
    for(i=0;i<n;i++)person[i]=i+1;
    whoIsTheLastOne(person,n);
    return 0;
}