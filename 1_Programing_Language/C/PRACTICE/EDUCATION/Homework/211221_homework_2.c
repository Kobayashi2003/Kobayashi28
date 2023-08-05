/*写一函数，实现两个字符串的比较。即自己写一个strcmp函数，函数原型为
int strcmp(char *p1, char *p2);
设p1指向字符串s1, p2指向字符串s2。要求当s1=s2时，返回值为0；若s1!=s2,返回它们二者第一个不同字符的ASCII码的差值（如"BOY" 与"BAD"，第二个字母不同，O与A之差为79-65=14）。 如果s1>s2，则输出正值；如果s1<s2，则输出负值。
（要求用指针方法处理）
*/
#include<stdio.h>
int Strcmp(char *p1,char *p2)
{
    while(*p1!='\0'&&*p2!='\0'&&*p1==*p2){//使用循环令指针向后移动 直到首次在对应位置出现不相同的字符或到达任意一方的尾部时终止
        p1++;
        p2++;
    }
    if(*p1!='\0'||*p1>*p2)return *p1-*p2;//当str2比str1先终止或当前str1对应位置上的字符大于str2对应的字符时 str1大于str2 返回两者当前字符ASCII值差 其值为正
    else if(*p2!='\0'||*p2>*p1)return *p1-*p2;//与上述相反
    return 0;
}
int main()
{
    char *str1="China",*str2="Chin";
    printf("%d\n",Strcmp(str1,str2));
    return 0;
}


/*
#include<stdio.h>
int Strcmp(char *p1,char *p2)
{
    while(*p1!='\0'&&*p2!='\0'&&*p1==*p2){
        p1++;
        p2++;
    }
    if(*p1!='\0'||*p1>*p2)return *p1-*p2;
    else if(*p2!='\0'||*p2>*p1)return *p1-*p2;
    return 0;
}
int main()
{
    char *str1="China",*str2="Chin";
    printf("the result from the function \"Strcmp\" is:%d\n",Strcmp(str1,str2));
    return 0;
}
*/