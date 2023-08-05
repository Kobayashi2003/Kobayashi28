#include<stdio.h>
#include<time.h>
#define N 10
void selectIntersection(int *array_1,int *array_2,int n1,int n2)
{
    printf("The Intersection Is:\n");
    for(int i=0;i<n1;i++)
        for(int j=0;j<n2;j++)
            if(array_1[i]==array_2[j])
            {
                printf("%-2d",array_1[i]);
                int temp=array_2[j];
                array_2[j]=array_2[n2-1];
                array_2[n2-1]=temp;
                n2--;
            }
}
int main()
{
    int array_1[N]={0},array_2[N]={0};
    int n1,n2;
    printf("Please enter the number of elements in the first array:\n");
    scanf("%d",&n1);
    printf("Please enter the elements in the first array:\n");
    for(int i=0;i<n1;i++)
        scanf("%d",&array_1[i]);
    printf("Please enter the number of elements in the second array:\n");
    scanf("%d",&n2);
    printf("Please enter the elements in the second array:\n");
    for(int i=0;i<n2;i++)
        scanf("%d",&array_2[i]);
    selectIntersection(array_1,array_2,n1,n2);
    return 0;
}