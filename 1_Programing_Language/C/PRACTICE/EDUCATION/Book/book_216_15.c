#include<stdio.h>
#define N 10
enum {error,normal}state;
void Input(int *num,char (*name)[N])
{
    for(int i=0;i<N;i++)
    {
        printf("Please enter the job number of the %d taff:\n",i+1);
        scanf("%d",&num[i]);
        printf("Please enter the name of the %d staff:\n",i+1);
        scanf("%s",name[i]);
    }
}
void Sort(int *num,char (*name)[N])
{
    int num_temp;
    char name_temp;
    for(int start=0;start<N-1;start++)
        for(int i=start;i<N;i++)
        {
            if(num[start]>num[i])
            {
                num_temp=num[start];
                num[start]=num[i];
                num[i]=num_temp;
                for(int j=0;j<N;j++)
                {
                   name_temp=name[start][j];
                   name[start][j]=name[i][j];
                   name[i][j]=name_temp;
                }
            }
        }
}
void binarySearch(int number,int left,int right,int *num,char (*name)[N]) 
{
    state=error;
    int mid=(num[left]+num[right])/2;
    if(number==mid)
    {
        printf("%d\n%s\n",mid,name[(left+right)/2]);
        state=normal;
    }
    else if(mid!=num[left]||mid!=num[right])
        switch(number>mid)
        {
            case 1:
            if(number==num[left])
            {
                printf("The guy whose job number is%d\n is:%s\n",num[left],name[left]);
                break;
            }
            binarySearch(number,mid,right,num,name);
            break;
            case 0:
            if(number==num[right])
            {
                printf("The guy whose job number is%d\n is:%s\n",num[right],name[right]);
                break;
            }
            binarySearch(number,left,mid,num,name);
            break;
        }
}
int main()
{
    int number;
    int num[N]={0};
    char name[N][N]={'\0'};
    Input(num,name);
    Sort(num,name);
    printf("Please enter the job number of the staff:\n");
    scanf("%d",&number);
    binarySearch(number,0,N-1,num,name);
    if(state==error)printf("There is no this GUY!!\n");
    return 0;
}