//输入十个数，从小到大将将它们输出
#include<stdio.h>
void Input(int *array)
{
    for(int i=0;i<10;i++)
        scanf("%d",&array[i]);
}
void Output(int *array)
{
    for(int i=0;i<10;i++)
        printf("%d ",array[i]);
}
void Bubble_Sort_Method(int *array)
{
    for(int i=0;i<9;i++)
        for(int j=0;j<9-i;j++)
            if(array[j]>array[j+1])
            {
                int temp=array[j];
                array[j]=array[j+1];
                array[j+1]=temp;
            }    
}
int main()
{
    int array[10];
    Input(array);
    Bubble_Sort_Method(array);
    Output(array);
    return 0;
}