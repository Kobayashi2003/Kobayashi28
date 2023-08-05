//选择法排序
#include<stdio.h>
void sort(int *c)
{
    for(int i=0;i<10;i++) 
    {
        int min=c[i];
        for(int j=i+1;j<10;j++)
            if(c[j]<min)
            {
                int temp=min;
                min=c[j];
                c[j]=temp;
            }
        c[i]=min;
    }
}
int main()
{
    int c[10];
    for(int i=0;i<10;i++)
        scanf("%d",&c[i]);
    sort(c);
    printf("From the min to the max:\n");
    for(int i=0;i<10;i++)
        printf("%d ",c[i]);
    return 0;
}