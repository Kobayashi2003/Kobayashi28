#include <stdio.h>
#include <string.h>
#define N 5
void Move(char *str, int n, int m)
{
    char end=*(str+n-1);
    for(char *p=str+n-1;p>str;p--)*p=*(p-1);
    *str=end;
    if(m>0)
    Move(str,n,m-1);
}
int main()
{
    int m;
    char str[N] = {'\0'};
    printf("Please enter the string:\n");
    scanf("%s", str);
    printf("Please enter an integer number:\n");
    scanf("%d", &m);
    Move(str,strlen(str),m);
    printf("The new string:\n%s\n",str);
    return 0;
}