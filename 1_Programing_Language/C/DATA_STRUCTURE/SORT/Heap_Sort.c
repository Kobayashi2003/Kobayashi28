#include<stdio.h>
void display(int array[],int size)  
{
    for(int i=0;i<size;i++)
    {
        printf("%d ",array[i]);
    }
    printf("\n");
}
void swap(int *array,int x,int y)
{
    int key=array[x];
    array[x]=array[y];
    array[y]=key;
}
void Down(int array[],int i,int n)
{
    int parent=i;
    int child=2*i+1;
    while(child<n)
    {
        if(child+1<n&&array[child]<array[child+1])
        {
            child++;
        }
        if(array[parent]<array[child])
        {
            swap(array,parent,child);
            parent=child;
        }
        child=child*2+1;
    }
}
void BuildHeap(int array[],int size)
{
    for(int i=size/2-1;i>=0;i--)
    {
        Down(array,i,size);
    }
}
void HeapSort(int array[],int size)
{
    printf("初始化数组:");
    BuildHeap(array,size);
    display(array,size);
    for(int i=size-1;i>0;i--)
    {
        swap(array,0,i);
        Down(array,0,i);
        printf("排序的数组:");
        display(array,size);
    }
}
int main()
{
    int array[]={1,2,3,4,5,6,7,8,9,10};
    int size=sizeof(array)/sizeof(int);
    printf("排序前的数组:");
    display(array,size);
    HeapSort(array,size);
    return 0;
}