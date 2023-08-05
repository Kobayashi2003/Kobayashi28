#include<stdio.h>
#define N 10
#define MARK 1
int main()
{
    int markTable[N]={0},n,n_temp,num=0,person;
    scanf("%d",&n);
    n_temp=n;
    for(person=0;n-1;person=(person+1)%n_temp)
    {
        if(markTable[person]==MARK)continue;
        if((++num)%3==0)
        {
            markTable[person]=MARK;
            n--;
        }
    }
    for(int i=0;i<n_temp;i++)
        if(markTable[i]!=MARK)printf("The last person is: %d\n",i+1);
    return 0;
}