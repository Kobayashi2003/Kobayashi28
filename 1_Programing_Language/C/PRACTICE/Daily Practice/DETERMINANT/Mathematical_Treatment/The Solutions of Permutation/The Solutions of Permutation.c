#include<stdio.h>

    int a[20];
    int n;

void showArray(int *a)
{
    int i;
    for(i=1;i<=n;i++)
    printf("%d",a[i]);
    printf("\n");
}

int main()
{
    extern void overturn();
    extern void changeSite();
    extern void ordinal();

	int i;
	char str[20];
	for(i=1;i<=4;i++)
		a[i]=i;
	a[0]=n=4;
	printf("对1234这四个数进行全排列\n");
	printf("翻转法:\n");
	overturn();
	printf("换位法:\n");
	changeSite();
	printf("序数法:\n");
	for(i=0;i<n;i++)
		str[i]=a[i+1]+'0';
	str[i]=0;
	ordinal(str,0,n);

    return 0;
}