#include<stdio.h>
int main()
{
    char c;
    int numbers=0,blanks=0,letters=0,others=0; //定义四个整型变量用以计数
    while((c=getchar())!='\n')  //定义一个字符变量c，并从键盘输入一个字符并将其赋给c，若c不为'\n',则判断此时的c属于哪一种字符，并用对应整型变量对此记数计数后继续该循环；若输入的为'\n'，则结束该循环，并输出各种字符的个数
    {
        if(c==' ')blanks++; 
        else if(c>='0'&&c<='9')numbers++;
        else if((c>='a'&&c<='z')||(c>='A'&&c<='Z'))letters++;
        else others++;
    }
    printf("数字的个数为：%d\n英文字母的个数为：%d\n空格的个数为：%d\n其他字符的个数为：%d\n",numbers,letters,blanks,others);
    return 0;
}