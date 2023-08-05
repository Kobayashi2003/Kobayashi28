//saddle point 该行最大，该列最小
#include<stdio.h>
int main()
{
    int count,a[2][2]={{1,2},{1,2}};
    for(int i=0; i<2; i++)
        for(int j=0; j<2; j++)
        {
            int temp=0;
            for(int k=0;k<2;k++)
            {
                if(a[i][k]>a[i][j])temp++;
                if(a[k][j]<a[i][j])temp++;
            }
            if(temp==0)printf("the %d saddle point is:%d\n",++count,a[i][j]);
        }
    if(count==0)printf("NO SADDLE NUMBER!\n");
    return 0;

}