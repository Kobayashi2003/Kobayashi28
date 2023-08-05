/*
输入现在的输入进制x和目标进制y，输入一个正整数n，x>=2，y<=36,n可以用阿拉伯数字和大写英文字母表示。
输入：x y n
输出：用目标进制表示的n
*/

//A 65 Z 90
//0 48 1 49 9 57

#include<stdio.h>
#include<math.h>
int main()
{
    int x,y;
    printf("请输入现在的输入进制\n");
    scanf("%d",&x);
    printf("请输入目标进制\n");
    scanf("%d",&y);
    getchar();

    printf("请输入需要转换的数字\n");
    char c[2000];
    int count=0;//用于计算转换为十进制后数字的位数
    for(int i=0;i<2000;i++)
    {
        c[i]=getchar();
        if(c[i]=='\n')
        break;
        count++;
    }

    int num=0;//先将该数转换为十进制

    int a,b;

    for(int i=0;i<count;i++)
    {
        if(c[i]>=48&&c[i]<=57)
        {
            c[i]=c[i]-48;
            a=pow(x,count-i-1);
            num=num+a*c[i];
        }
        if(c[i]>=65&&c[i]<=90)
        {
            c[i]=c[i]-55;
            b=pow(x,count-i-1);
            num=num+b*c[i];
        }
    }

    printf("先转换为十进制%d\n",num);

    //将十进制的数转换为目标进制后输出
    //先算出转换进制后数的长度

    int figure=1;
    int temp1;
    temp1=num/pow(y,figure);
    while(temp1!=0)
    {
        figure++;
        temp1=num/pow(y,figure);
    }  
    printf("转换后位数%d\n",figure);

    //接下来分别求出每一位上的数字并将其输出

    int temp2;
    int num_each;
    while(figure>0)
    {
        num_each=0;
        temp2=num;
        while(temp2>0)
        {
            temp2=num-num_each*pow(y,figure-1);

            if(temp2>0)
            {
                num_each++;
            }
            
            else if(temp2==0)
            {
                break;
            }

            else(temp2<0)
            {
                num_each--;
                break;
            }
            
        }

        num=num-num_each*pow(y,figure-1);

        //接下来将每位上的数字进行调整后输出
        if(num_each>=0&&num_each<=9)
        {
            num_each=num_each+48;
        }

        if(num_each>=10&&num_each<=35)
        {
            num_each=num_each+55;
        }

        printf("%c",num_each);


        figure--;
    }
    return 0;
}