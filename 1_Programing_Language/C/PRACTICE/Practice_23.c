#include<stdio.h>
#define N
#define FIN 2
void Change(int num)
{
    if(num>=FIN) Change(num/FIN);
    printf("%c",(num%FIN<10)?num%FIN+'0':num%FIN+'A'-10);
}
int main()
{
    int num;
    scanf("%d",&num);
    Change(num);
    return 0;
}