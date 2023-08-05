// 2022/6/4 用于将一串字符串根据ASCII转换为二进制码
#include <stdio.h>
#define N 50
#define MAX(x,y) (x>y)?x:y
int main()
{
    char str[] = "cyber_security";
    for (int len = 0; len < sizeof(str) - 1 / sizeof(char); len++)
    {
        int num[N] = {0}, sum = (int)str[len], cont = 0;
        while (sum)
        {
            int ord = 0;
            num[ord]++;
            sum--;
            while (num[ord] - 2 == 0)
            {
                num[ord] = 0;
                num[++ord]++;
                cont = MAX(ord, cont);
            }
        }
        for (int i = cont; i >= 0; i--)
        {
            printf("%c", num[i] + ((num[i] >= 0 && num[i] <= 9) ? '0' : 'A' - 10));
        }
    }
    return 0;
}