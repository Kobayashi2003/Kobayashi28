#include<stdio.h>
#include<math.h>
int main()
{
    int num;
    scanf("%d",&num);

    int tem1,i=1;

    part1:

    tem1=num-(int)pow(10,i);

    if(tem1>=0)
    {
        i=i+1;
        goto part1;
    }

    printf("该数是%d位数\n",i);
    int j;
    j=i;
    int tem2,a=1;

    part2:

    tem2=num-a*(int)pow(10,i-1);

    if(tem2>=0)
    {
        a=a+1;
        goto part2;
    }

    int b[10];

    if(tem2<0)
    {
        b[i]=a-1;
        printf("%d\n",b[i]);
        num=num-(a-1)*(int)pow(10,i-1);
        i=i-1;
        a=1;

        if(i<=0)
        {
        goto part3;
        }
        goto part2;
    }

    part3:
    
    printf("该数的逆序为\n");
    for(int k=1;k<=j;k++)
    {
        printf("%d",b[k]);
    }

    return 0;
}
