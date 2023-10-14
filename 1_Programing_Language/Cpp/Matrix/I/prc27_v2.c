#include <stdio.h>
#include <string.h>

#define N1 201 // 字符串长度最长为200
#define N2 11 // 分隔符最长为10
#define COUNT 20 // 分隔后字符串数量最多为20

/*
函数：split
输入：原字符串origin，分隔符sep，以及存放结果的二维输入result
    result的使用方法：例如strcpy(result[i],aimStr)可以将aimStr的值导入到result的第i个位置，其中aimStr为计算出的字符串。之后调整i即可
输出：分隔出的字符串的数量。
功能：
    根据分隔符sep切分给定的原字符串origin，并返回分隔后的字符串的数量。
    举个例子："123045607890"，分隔符为"0"，则返回值为4，result={"123","456","789",""}
*/

void get_next(char *p, int *next) {
    int i = 0, j = -1;
    next[0] = -1;
    while (p[i] != '\0') {
        if (j == -1 || p[i] == p[j]) {
            i++;
            j++;
            next[i] = j;
        } else {
            j = next[j];
        }
    }
}

int kmp(char *s, char *p, int *next) {
    int len1 = 0, len2 = 0;
    while (s[len1] != '\0') len1++;
    while (p[len2] != '\0') len2++;

    for (int i = 0, j = 0; i < len1; i++) {
        while (j > 0 && s[i] != p[j]) j = next[j];
        if (s[i] == p[j]) j++;
        if (j == len2) return i - len2 + 1;
    }

    return -1;
}

int split(char origin[], char sep[],char (*result)[N1]) {

    origin[strlen(origin)] = '\0';
    sep[strlen(sep)] = '\0';

    int count = 0;

    char *p = origin;
    int next[N2] = {0};
    get_next(sep, next);

    int pos = kmp(p, sep, next);
    while (pos != -1) {
        strncpy(result[count], p, pos);
        result[count][pos] = '\0';
        count++;
        p += pos + strlen(sep);
        pos = kmp(p, sep, next);
    }
    strcpy(result[count], p);
    count++;

    return count;
}

int main(void){

    char origin[N1];
    char sep[N2];
    char result[COUNT][N1];

    gets(origin);
    gets(sep);
    int n_result = split(origin,sep,result);
    int i;
    for(i=0;i<n_result;i++){
        printf("%s\n",result[i]);
    }
    return 0;
}