//AB*CD=BA*DC
//其中ABCD分别代表一位数字
//注意到ABCD都不能为0
//另限制ABCD互不相等
#include<stdio.h>
int main()
{
    for(int A=1;A<10;A++)
    {
        for(int B=1;B<10;B++)
        {
            if(B==A) continue;
            for(int C=1;C<10;C++)
            {
                if(C==B||C==A) continue;
                for(int D=1;D<10;D++)
                {
                    if(D==C||D==B||D==A) continue;
                    if((10*A+B)*(10*C+D)==(10*B+A)*(10*D+C))
                    {
                        printf("%d%d*%d%d==%d%d*%d%d result:%d\n",A,B,C,D,B,A,D,C,(10*A+B)*(10*C+D));
                    }
                }
            }
        }
    }
}