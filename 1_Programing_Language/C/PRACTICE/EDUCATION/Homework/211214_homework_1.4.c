#include<stdio.h>
int main()
{
    int *p,i,a[10];
    p=a;
    printf("please enter 10 ingeter numbers:");
    for(i=0;i<10;i++)
        scanf("%d",p++);
    p=a;
    for(i=0;i<10;i++,p++)
        printf("%d ",*p);
    printf("\n");
    return 0;
}