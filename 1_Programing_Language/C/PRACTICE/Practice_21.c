//选出一个数组中最小的两个数
#include <stdio.h>
#define MAX 99999
int main()
{
    int array[] = {1, 2, 34, 5, 0};
    int a = MAX, b = MAX;
    for (int i = 0; i < sizeof(array) / sizeof(int); i++)
    {
        if (array[i] < a)
        {
            b = a;
            a = array[i];
        }
        else if (array[i] < b)
        {
            b = array[i];
        }
    }
    printf("%d %d", a, b);
    return 0;
}