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
void Selection_Sort(int *array)
{
    for(int i=0;i<9;i++)
        for(int j=i+1;j<10;j++)
            if(array[j]<array[i])
            {
                int temp=array[j];
                array[j]=array[i];
                array[i]=temp;
            }
}
int main()
{
    int array[10];
    Input(array);
    Selection_Sort(array);
    Output(array);
}