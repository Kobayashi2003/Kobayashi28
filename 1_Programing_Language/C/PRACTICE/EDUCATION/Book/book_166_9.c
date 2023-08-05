#include<stdio.h>
#define Both_Ture 2
#define One_Ture 1
#define Both_False 0
void Bisearch_Binary_Search(int *array,int num,int left_endpoint,int right_endpoint,int *p_buffer)
{
    switch((num>=array[(left_endpoint+right_endpoint)/2])+(num==array[(left_endpoint+right_endpoint)/2]))
    {
        case Both_Ture:
            printf("this num is the %d number of array\n",(left_endpoint+right_endpoint)/2+1);
            (*p_buffer)++;
            break;
        case One_Ture:
            if(left_endpoint!=(left_endpoint+right_endpoint)/2)Bisearch_Binary_Search(array,num,(left_endpoint+right_endpoint)/2,right_endpoint,p_buffer);
            break;
        case Both_False:             
            if(left_endpoint!=(left_endpoint+right_endpoint)/2)Bisearch_Binary_Search(array,num,left_endpoint,(left_endpoint+right_endpoint)/2,p_buffer);
            break;
    }
}
int main()
{
    int array[15]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14},num,buffer=0;
    int *p_buffer=&buffer;
    scanf("%d",&num);
    Bisearch_Binary_Search(array,num,array[0]-1,array[14]+1,p_buffer);
    if(buffer==0)printf("The array doesn't contain this number!\n");
    return 0;
}