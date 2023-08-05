#include<stdio.h>

int change(char c)
{
    if(c<=91&&c>=65)
    c=c+32;
    return c;
}

int main()
{
    printf("Please input first character\n");
    char c1,c2;
    scanf("%c",&c1);
    c1=change(c1);

    switch(c1)
    {
        case('m'):printf("Monday\n");break;
        case('w'):printf("Wednesday\n");break;
        case('f'):printf("Friday\n");break;

        case('t'):
            {
                printf("Please input second character\n");
                getchar();
                scanf("%c",&c2);
                c2=change(c2);
                switch(c2)
                {
                    case('u'):printf("Tuesday\n");break;
                    case('h'):printf("Thursday\n");break;
                    default:printf("illegal input!\n");break;
                }
                break;
            }

        case('s'):
            {
                printf("Please input second character\n");
                getchar();
                scanf("%c",&c2);
                c2=change(c2);
                switch(c2)
                {
                    case('u'):printf("Sunday\n");break;
                    case('a'):printf("Saturday\n");break;
                    default:printf("illegal input!\n");break;
                }
                break;
            }

        default:
            {
                printf("illegal input!\n");
            }
    }

    return 0;
}

