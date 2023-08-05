/*
给出一百分制成绩，要求输出成绩'A', 'B', 'C', 'D', 'E'。
90分以上为'A', 80~89分为'B', 70~79为'C', 60~69分为'D', 60分以下为'E'。
要求用switch语句实现
*/

#include<stdio.h>
int main()
{
    int grade;
    int temp;
    printf("Please input the grade\n");
    scanf("%d", &grade);
    temp=grade>=90;//判断该成绩是否不小于90，若为真，则将1赋值给temp；若为假，则将0赋值给temp
    switch(temp)
    {
        case 1:
        printf("A");
        break;

        case 0:
        temp=grade>=80;
        switch(temp)
        {
            case 1:
            printf("B");
            break;

            case 0:
            temp=grade>=70;
            switch(temp)
            {
                case 1:
                printf("C");
                break;

                case 0:
                temp=grade>=60;
                switch(temp)
                {
                    case 1:
                    printf("D");
                    break;

                    case 0:
                    printf("E");
                    break;
                }
                break;
            }
            break;
        }
        break;
    }

    return 0;
}