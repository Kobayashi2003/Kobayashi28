/*
 输入字母判断是星期几例如： 
 程序运行时，提示你"please input first character:
 "你输入'f'或者'F'，则程序输出"Friday"，
 你输入s，则程序进一步提示你"Please input second character:"
 此时还需要进一步输入u，程序才输出"Sunday"
 如果你输入的字母和任何星期的英文单词首字母都不匹配，则程序需要提示"Illegal input!\n"。
 */

#include<stdio.h>

int change(char c)
{
    if(c<=91&&c>=65)
    c=c+32;
    return c;
}
int main()
{
    char c1,c2;
    printf("please input the first character\n");
    scanf("%c",&c1);
    c1=change(c1);

    if(c1=='m')
    printf("Monday\n");

    else if(c1=='w')
    printf("Wednesday\n");

    else if(c1=='f')
    printf("Friday\n");

    else if(c1=='s')
    {
        printf("please input the second character\n");

        getchar();
        scanf("%c",&c2);
        c2=change(c2);

        if(c2=='u')
        printf("Sunday\n");

        else if(c2=='a')
        printf("Saturday\n");

        else
        printf("illegal input!\n");
    }  

        else if(c1=='t')
    {
        printf("please input the second character\n");

        getchar();
        scanf("%c",&c2);
        c2=change(c2);

        if(c2=='u')
        printf("Tuesday\n");

        else if(c2=='h')
        printf("Thursday\n");

        else
        printf("illegal input!\n");
    }  

    else 
    printf("illegal input!\n");

    return 0;
}

/*
关于getchar的作用

1.从缓冲区读走一个字符，相当于清除缓冲区  
  
2.前面的scanf()在读取输入时会在缓冲区中留下一个字符'\n'（输入完s[i]的值后按回车键所致），所以如果不在此加一个
getchar()把这个回车符取走的话，gets(）就不会等待从键盘键入字符，而是会直接取走这个“无用的”回车符，从而导致读取有误  
  
3.  
getchar()是在输入缓冲区顺序读入一个字符(包括空格、回车和Tab)  
getchar()使用不方便,解决方法：   
（1）使用下面的语句清除回车：   
while(getchar()!='\n');   
（2）用getche()或getch()代替getchar()，其作用是从键盘读入一个字符（不用按回车），注意要包含头文件<conio.h>  
  
4. 
getchar()是stdio.h中的库函数，它的作用是从stdin流中读入一个字符，也就是说，如果stdin有数据的话不用输入它就可以直接
读取了，第一次getchar()时，确实需要人工的输入，但是如果你输了多个字符，以后的getchar()再执行时就会直接从缓冲区中读
取了。  
实际上是 输入设备->内存缓冲区->程序getchar    
你按的键是放进缓冲区了,然后供程序getchar
*/


