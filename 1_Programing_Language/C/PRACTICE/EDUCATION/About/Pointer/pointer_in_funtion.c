#include<stdio.h>
#define N 10
void pointer1(int (*p1)[N])
{
    printf("the pointer1 is:%p\n",p1);
}

void pointer2(int p2[][N])
{
    printf("the pointer2 is:%p\n",p2);
}

void pointer3(int *p3)
{
    printf("the pointer3 is:%p\n",p3);
}

void pointer4(int *p4)
{
    printf("the pointer4 is:%p\n",p4);
}

void pointer5(int (*p5)[N])
{
    printf("the pointer5 is:%p\n",p5);
}

void pointer6(int *p6)
{
    printf("the pointer6 is:%p\n",p6);
}

void pointer7(int **p7)
{
    printf("the pointer7 is:%p\n",p7);
}

void pointer8(int *p8[])
{
    printf("the pointer8 is:%p\n",p8);
}

void symbol()
{
    return;
}

void pointer9(void (*p9)(void))
{
    printf("the pointer9 is:%p\n",p9);
}

int main()
{
    int array[N][N];
    for(int i=0;i<N;i++)
        for(int j=0;j<N;j++)
            array[i][j]=i+j;

    

    pointer1(array);
    pointer2(array);

    pointer3(array[0]);
    pointer4(&array[0][0]);

    pointer5(&array[0]);
    pointer6(*array);

    printf("\n\n");

    pointer1(array+1);
    pointer2(array+2);

    pointer3(array[0]+1);
    pointer4(&array[0][0]+2);

    pointer5(&array[0]+1);
    pointer6(*array+1);

    printf("\n\n");    

    int *p[N]={NULL};
    pointer7(p);
    pointer8(&p[0]);

    pointer9(symbol);

    return 0;
}

