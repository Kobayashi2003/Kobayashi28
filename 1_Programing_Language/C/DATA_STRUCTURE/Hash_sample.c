#include<stdio.h>
#define MAX_TABLE_SIZE 100//哈希表的最大长度
#define N 10
void create_hash(int a[],int n,int table[])
{
    for(int i=0;i<n;i++)table[a[i]]++;
}
int find_key(int table[],int key)
{
    return table[key]!=0;
}
int main()
{
    int a[N]={1,2,3,4,5,6,7,8,9,10};
    int table[MAX_TABLE_SIZE]={0};
    create_hash(a,N,table);
    for(int i=0;i<MAX_TABLE_SIZE;i++)
        if(table[i]>0)printf("%d appear %d times\n",i,table[i]);
    printf("test:\n");
    
    for(int i=1;i<10;i++)
    {
        if(find_key(table,i))printf("%d is in the array.\n",i);
        else printf("%d is not in the array.\n",i);
    }
    return 0;
}