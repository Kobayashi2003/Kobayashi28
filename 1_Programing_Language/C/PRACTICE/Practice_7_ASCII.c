#include<stdio.h>
#include<string.h>
#define N 50
#define CARRY num[ord]-n2==0
#define MAX(x,y) (x>y)?x:y
int main()
{
	char str1[N]={'\0'};
	int num[N]={0},sum=0,n1,n2,ord,cont=0;
	scanf("%d%d",&n1,&n2);
	scanf("%s",str1);
	strupr(str1);
	for(int i=0;i<strlen(str1);i++)
		sum=n1*sum+((str1[i]>='0'&&str1[i]<='9')?str1[i]-'0':str1[i]-'A'+10);
	while(sum)
	{
		ord=0;
		num[ord]++;
		sum--;
		while(CARRY)
		{
			num[ord]=0;
			num[++ord]++;
			cont=MAX(ord,cont);
		}
	}
	for(int i=cont;i>=0;i--)
		printf("%c",num[i]+((num[i]>=0&&num[i]<=9)?'0':'A'-10));
	return 0;
}