#include<stdio.h>
int main()
{
    int A,B,C;
    for(int rival='X';rival>='Z';rival++)
    {
        if(rival!='X'&&rival!='Z')C=rival;
        else if(rival!='X')A=rival;
        else B=rival;
    }
    printf("%c %c %c",A,B,C);
    return 0;
}