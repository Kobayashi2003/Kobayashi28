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
void Insertion_Sort(int *array)
{
    for(int i=1;i<10;i++)
    {
        int count=0;
        for(int j=0;j<i;j++)
            if(array[i]>array[j])count++;
        int temp=array[i];
        for(int k=i;k>count;k--)
            array[k]=array[k-1];
        array[count]=temp;
    }       
}
int main()
{
    int array[10];
    Input(array);
    Insertion_Sort(array);
    Output(array);
    return 0;
}