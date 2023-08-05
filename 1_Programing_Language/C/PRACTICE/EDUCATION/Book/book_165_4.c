#include<stdio.h>
void Put(int array[],int n)
{
    for(int i=0;i<n;i++)
        printf("%d ",array[i]);
    putchar('\n');
}
void Inset(int ori[],int array[],int num)
{
    int count=0;
    for(int i=0;i<9;i++)
        if(num>ori[i])count++;
    for(int i=0,j=0;i<10;i++,j++)
    {
        if(i==count)
        {
            array[i]=num;
            j--;
            continue;
        }
        array[i]=ori[j];
    }
}
int main()
{
    printf("The original array:\n");
    int num,ori[]={1,2,3,4,5,6,7,8,10},array[10]={0};
    Put(ori,9);
    printf("Please input a number:");
    scanf("%d",&num);
    Inset(ori,array,num);
    Put(array,10);
    return 0;
}