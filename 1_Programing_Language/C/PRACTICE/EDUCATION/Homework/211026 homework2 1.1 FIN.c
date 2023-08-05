#include<stdio.h>
int main()
{
    int num;
    scanf("%d",&num);

    int a[5];
    int j;//定义变量j，用于确定最后输出数组a[i]中元素的个数
    
    if(num>=10000)
    {
        printf("该数为五位数\n");
        j=1;

        a[5]=num/10000;
        num=num-a[5]*10000;
        printf("万分数为%d\n",a[5]);
        goto part1;
    }

    if(num>=1000)
    {
        printf("该数为四位数\n");
        j=4;
        
        part1:

        a[4]=num/1000;
        num=num-a[4]*1000;
        printf("千分数为%d\n",a[4]);

        goto part2;
    }

    if(num>=100)
    {
        printf("该数为三位数\n");
        j=3;
       
        part2: 

        a[3]=num/100;
        num=num-a[3]*100;
        printf("百分位为%d\n",a[3]);

        goto part3;
    }

    if(num>=10)
    {
        printf("该数为二位数\n");
        j=2;
        
        part3: 

        a[2]=num/10;
        num=num-a[2]*10;
        printf("十分位为%d\n",a[2]);

        goto part4;
    }

    if(num>=0)
    {
        printf("该数为个位数\n");
        j=1;
        
        part4:

        a[1]=num;
        printf("个位为%d\n",a[1]); 
    }

    printf("该数的逆序为");
    for(int i=1;i<=j;i++)
        printf("%d",a[i]);
        
    return 0;
}