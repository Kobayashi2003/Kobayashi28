#include<stdio.h>
int main()
{
	int a, b, c, d, max,min;
	printf("please in put a,b,c,d:\n");
	scanf_s("%d,%d,%d,%d", &a, &b, &c, &d);
	max = a;
	if (max < b)
		max = b;
	if (max < c)
		max = c;
	if (max < d)
		max = d;
	printf("max=%d\n",max);
    min=a;
    if(min>b)
    min=b;
    if(min>c)
    min=c;
    if(min>d)
    min=d;
    printf("min=%d",min);
	return 0;
}
