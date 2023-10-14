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
int split(char origin[], char sep[],char (*result)[N1]) {
    int count = 0;
    
    char *p = strtok(origin,sep);

    while(p != NULL){
        strcpy(result[count++],p);
        p = strtok(NULL,sep);
    }

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