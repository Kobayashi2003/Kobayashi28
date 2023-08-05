#include<stdio.h>
#include<string.h>
#define N 4
void OutPut_with_Blank(char *array)
{
    for(int i=0;i<N;i++,putchar(' '))
        printf("%c",array[i]);
}
int main()
{
    char array[N];
    gets(array);
    OutPut_with_Blank(array);
    return 0;
}
//您拿外部函数搁这儿干这个呢？