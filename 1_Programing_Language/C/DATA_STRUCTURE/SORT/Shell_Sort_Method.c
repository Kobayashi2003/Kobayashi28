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
void Shell_Sorted(int *array)
{
    
}
int main()
{
    int array[10];
    Input(array);
    Sell_Sort(array);
    Out(array);
    return 0;
}