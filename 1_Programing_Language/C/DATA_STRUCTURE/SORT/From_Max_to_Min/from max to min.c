#include<stdio.h>
int main()
{
    int a, b, c, d, e, f;
    scanf_s("%d,%d,%d,%d,%d,%d", &a, &b, &c, &d, &e, &f);

    int max1;

    max1 = a;;
    if (max1 < b)
        max1 = b;
    if (max1 < c)
        max1 = c;
    if (max1 < d)
        max1 = d;
    if (max1 < e)
        max1 = e;
    if (max1 < f)
        max1 = f;

    int x = 0;
    int temp;

    if (a == max1)
        x = x + 1;
    if (b == max1)
        x = x + 1;
    if (c == max1)
        x = x + 1;
    if (d == max1)
        x = x + 1;
    if (e == max1)
        x = x + 1;
    if (f == max1)
        x = x + 1;

    temp = x;

    while (x > 0)
    {
        printf("%d\n", max1);
        x = x - 1;
    }

    int max2;

    for (int y = 6 - temp; y > 0; y--)
    {
        if (a < max1)
            max2 = a;
        if (b < max1)
            max2 = b;
        if (c < max1)
            max2 = c;
        if (d < max1)
            max2 = d;
        if (e < max1)
            max2 = e;

        if (max2 < a && a < max1)
            max2 = a;
        if (max2 < b && b < max1)
            max2 = b;
        if (max2 < c && c < max1)
            max2 = c;
        if (max2 < d && d < max1)
            max2 = d;
        if (max2 < e && e < max1)
            max2 = e;
        if (max2 < f && f < max1)
            max2 = f;

        int z = 0;

        if (a == max2)
            z = z + 1;
        if (b == max2)
            z = z + 1;
        if (c == max2)
            z = z + 1;
        if (d == max2)
            z = z + 1;
        if (e == max2)
            z = z + 1;
        if (f == max2)
            z = z + 1;

        y = y - z + 1;

        while (z > 0)
        {
            printf("%d\n", max2);
            z = z - 1;
        }

        max1 = max2;

    }

    return 0;
}