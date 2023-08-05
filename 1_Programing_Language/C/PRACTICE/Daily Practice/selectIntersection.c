#include<stdio.h>
#define N 10
#define Mark 1
int isEmpty(int *Table)
{
    int count=0;
    for(int i=0;i<N;i++)
        if(Table[i]==Mark)count++;
    return count;
}
void selectIntersection(int *array_1,int *array_2,int n1,int n2)
{
    int Table[N]={0};
    for(int i=0;i<n1;i++)
        for(int j=0;j<n2;j++)
            if(array_1[i]==array_2[j])
            {
                if(Table[j]!=Mark)
                {
                    Table[j]=Mark;
                    break;
                }
            }
    if(isEmpty(Table)!=0)
    {
        for(int i=0;i<n1;i++)
            if(Table[i]==Mark)printf("%-2d",array_2[i]);
    }
    else printf("No Intersection!\n");
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

/*#include<stdio.h>
#define N 10
#define Mark 1
int main()
{
	int isEmpty(int *Table);
	void selectIntersection(int *array_1,int *array_2,int n1,int n2);
	int i;
    int array_1[N]={0},array_2[N]={0};
    int n1,n2;
    printf("Please enter the number of elements in the first array:\n");
    scanf("%d",&n1);
    printf("Please enter the elements in the first array:\n");
    for(i=0;i<n1;i++)
        scanf("%d",&array_1[i]);
    printf("Please enter the number of elements in the second array:\n");
    scanf("%d",&n2);
    printf("Please enter the elements in the second array:\n");
    for(i=0;i<n2;i++)
        scanf("%d",&array_2[i]);
    selectIntersection(array_1,array_2,n1,n2);
    return 0;
}
int isEmpty(int *Table)
{
	int i;
    int count=0;
    for(i=0;i<N;i++)
        if(Table[i]==Mark)count++;
    return count;
}
void selectIntersection(int *array_1,int *array_2,int n1,int n2)
{
	int i,j;
    int Table[N]={0};
    for(i=0;i<n1;i++)
        for(j=0;j<n2;j++)
            if(array_1[i]==array_2[j])
            {
                if(Table[j]!=Mark)
                {
                    Table[j]=Mark;
                    break;
                }
            }
    if(isEmpty(Table)!=0)
    {
		int i;
        for(i=0;i<n1;i++)
            if(Table[i]==Mark)printf("%-2d",array_2[i]);
    }
    else printf("No Intersection!\n");
}
*/