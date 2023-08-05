#include<stdio.h>
#include<time.h>
#include<stdlib.h>
int main()
{
    unsigned long long int i=time(NULL);
    int cont=10;
    while(cont)
    {
        if(time(NULL)-i==1)
        {
            printf("%d\n",cont--);
            i=time(NULL);
        }
    }
    printf("OVER");
    system("shutdown -s -t 0");
    return 0;
}