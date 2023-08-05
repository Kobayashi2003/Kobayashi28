#include<stdio.h>
void Compare(int *a,int *b,int *c)
{
    int *temp[]={a,b,c};
    for(int i=0;i<3;i++)
        for(int j=i;j<3;j++)
            if(*temp[i]>*temp[j])
            {
                *temp[i]^=*temp[j];
                *temp[j]^=*temp[i];
                *temp[i]^=*temp[j];
            }
}
int main()
{
    int a,b,c;
    scanf("%d%d%d",&a,&b,&c);
    int *pa=&a,*pb=&b,*pc=&c;
    Compare(pa,pb,pc);
    printf("%d %d %d",a,b,c);
    return 0;
}