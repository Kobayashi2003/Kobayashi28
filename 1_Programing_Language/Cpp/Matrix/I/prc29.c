#include <stdio.h>
#include <stdlib.h>
#include <string.h>

# define MAXN 201 // 最大字符串长度不超过100
# define MAXCOUNT 10 // 匹配次数不超过10次

// 提示：请自行设计测试用例，确保所实现的函数功能符合预期

/*
函数：try_concatenate
输入：字符串cache，字符串afterStr，字符ch，整数num
输出：无
功能：需要在字符串cache中产生num个字符ch，并于字符串afterStr进行拼接
    例如try_concatenate("","3456",'2',5)，cache的值在调用之后应当为"222223456"
*/
void try_concatenate(char cache[],char afterStr[],char ch,int num);

/*
函数：tail_string
输入：字符串ch1，字符串ch2，位置变量pos
输出：无
功能：将字符串ch2从位置pos及以后的字符拷贝到ch1中。
    例如tail_string("","01234567",3)，ch1的值在调用之后应当为"34567"
    题目保证，字符串ch1的长度足够长
补充：数组ch2的值不可发生任何更改。
*/
void tail_string(char ch1[], char ch2[], int pos);

/*
函数：plus_result
输入：字符串afterStr，字符串str，字符ch，函数指针judge
输出：如果能够匹配，则返回1；否则，返回0.
功能：
    该函数用于判断模糊匹配+的时候是否完全匹配，比如说对于给定正则表达式reg="1+23"和目标字符串str="1123"。
    此时，afterStr为之后的字符"23"，str即为要匹配的目标字符串；ch为模糊匹配符前的字符，这里为'1'，judge为一个能够判断给定的两个字符是否完全匹配的函数，详情见test.c中的question_result函数
    实现思路与question_result类似，但是+能够匹配1个到多个（最多为10个）字符
*/
int plus_result(char afterStr[], char str[], char ch,int (*judge)(char *, char *));

/*
函数：star_result
输入：字符串afterStr，字符串str，字符ch，函数指针judge
输出：如果能够匹配，则返回1；否则，返回0.
功能：
    该函数用于判断模糊匹配*的时候是否完全匹配，比如说对于给定正则表达式reg="1*23"和目标字符串str="1123"。
    此时，afterStr为之后的字符"23"，str即为要匹配的目标字符串；ch为模糊匹配符前的字符，这里为'1'，judge为一个能够判断给定的两个字符是否完全匹配的函数，详情见test.c中的question_result函数
    实现思路与question_result类似，但是*能够匹配0个到多个（最多为10个）字符
*/
int star_result(char afterStr[], char str[], char ch,int (*judge)(char *, char *));
/*
函数：question_result
输入：字符串afterStr，字符串str，字符ch，函数指针judge
输出：如果能够匹配，则返回1；否则，返回0.
功能：
    该函数用于判断模糊匹配?的时候是否完全匹配，比如说对于给定正则表达式reg="1?23"和目标字符串str="123"。
    此时，afterStr为之后的字符"23"，str即为要匹配的目标字符串；ch为模糊匹配符前的字符，这里为'1'，judge为一个能够判断给定的两个字符是否完全匹配的函数，具体实现见下面的judge函数（judge的实现细节与要实现的函数没有关系）
    实现思路为将模糊匹配转换为精确匹配，再逐个比较（暴力递归）
    具体思路见内部注释
*/

void try_concatenate(char cache[], char afterStr[], char ch, int num){
    for (int i = 0; i < num; ++i) 
        cache[i] = ch;
    while (*afterStr != '\0') {
        cache[num++] = *afterStr++;
    }
}

void tail_string(char ch1[], char ch2[], int pos) {
    int i = 0;
    while (ch2[pos] != '\0') {
        ch1[i++] = ch2[pos++];
    }
    ch1[i] = '\0';
}

int plus_result(char afterStr[], char str[], char ch, int (*judge)(char *, char *)) {
    char cache[MAXN];

    int result;

    memset(cache, 0, sizeof(cache));
    for (int i = 1; i <= MAXCOUNT; ++i) { // the situation of 1 to MAXCOUNT match
        try_concatenate(cache, afterStr, ch, i);
        result = judge(cache, str);
        if (result)
            return 1;
    }

    return 0; // the situation of no match
}

int star_result(char afterStr[], char str[], char ch, int (*judge)(char *, char *)) {
    char cache[MAXN];
    int result = judge(afterStr, str); // the situation of 0 match
    if (result)
        return 1;

    memset(cache, 0, sizeof(cache));
    for (int i = 1; i <= MAXCOUNT; ++i) { // the situation of 1 to MAXCOUNT match
        try_concatenate(cache, afterStr, ch, i);
        result = judge(cache, str);
        if (result)
            return 1;
    }

    return 0; // the situation of no match
}


int question_result(char afterStr[], char str[], char ch,int (*judging)(char *, char *)){
    // ? 可以匹配0/1个原字符
    char cache[MAXN];
    int result = judging(afterStr,str); // 匹配0个原字符的情况，得到afterStr。再运用judging判断afterStr与所给的str是否完全匹配
    if(result){ // 只要之后的所有情况中有一个匹配即可返回
        return 1;
    }
    // 如果没有，则匹配有1个原字符的情况
    int i=1;
    memset(cache,0,sizeof(cache)); // 将cache清空
    try_concatenate(cache,afterStr,ch,i); // 使用try_concatenate产生用于精确匹配的结果，以注释中的例子，try_concatenate("","23",'1',1)，之后cache为"123"
    result = judging(cache,str); // 尝试使用judging进行匹配，并将结果返回
    return result;
}

int validChar(char ch){
    if(ch<='9' && ch>='0'){
        return 1;
    }
    else if(ch>='a' && ch<='z'){
        return 1;
    }
    else if(ch>='A' && ch<='Z'){
        return 1;
    }
    else{
        return 0;
    }
}

/*
输入：正则字符串reg，要匹配的字符串str
输出：reg是否能完全匹配str，如果是，则返回1；如果否，则返回0。
功能：使用递归方法，判断给定的正则
*/
static int times = 0;
int judge(char reg[], char str[]){
    // 安全措施，防止爆栈
    times ++;
    if(times>20000){
        return -1;
    }
    int regLen = strlen(reg), strLen = strlen(str);
    // printf("judge %s(%d) %s(%d)\n",reg,regLen,str,strLen);
    // legal check
    if(regLen==0 || strLen==0){
        // printf("last: run out something %s %s\n",reg,str);
        if(regLen==0&&strLen==0){
            return 1;
        }else if(regLen==0){
            return 0;
        }else{ // regLen!=0 and strLen==0 此时后面可能有零匹配
            if(reg[0]=='+'||reg[0]=='*'||reg[0]=='?'){ // 最后刚好匹配上了
                if(regLen==1){
                    return 1;
                }else{
                    char ch1[MAXN];
                    memset(ch1,0,sizeof(ch1));
                    tail_string(ch1,reg,1);
                    return judge(ch1,str);
                }
            }
            else if(regLen>=2 && (reg[1]=='*' || reg[1]=='?')){
                char ch1[MAXN];
                memset(ch1,0,sizeof(ch1));
                tail_string(ch1,reg,2);
                return judge(ch1,str);
            }
            else{
                return 0;
            }
        }
    }
    // 如果当前表达式长度不足，进行最后一次精确匹配
    else if(regLen==1){
        // printf("last: only 1 length %s %s\n",reg,str);
        if(strLen>1){
            return 0;
        }
        if(reg[0]==str[0]){
            return 1;
        }else{
            return 0;
        }
    }

    // 如果能精确匹配
    int validResult = validChar(reg[1]);
    if(validResult){
        if(reg[0] == str[0]){
            //尝试进行后续匹配
            int i;
            for(i=1;i<strlen(reg)&&i<strlen(str);i++){
                if(reg[i]==str[i]){
                    continue;
                }else{
                    // printf("<%d> start: checking %s(%d) and %s(%d)\n",times,reg,strlen(reg),str,strlen(str));
                    // printf("<%d> start: checking %d %c\n",times,i,reg[i]);
                    //不匹配的原因
                    // 遇到特殊字符，回退，产生新的字符串，并请求。
                    if(!validChar(reg[i])){
                        char ch1[MAXN],ch2[MAXN];
                        memset(ch1,0,sizeof(ch1));
                        memset(ch2,0,sizeof(ch2));
                        tail_string(ch1,reg,i-1);
                        tail_string(ch2,str,i-1);
                        return judge(ch1,ch2);
                    }
                    // 当前失配不是特殊字符
                    else{
                        // 如果下一个是特殊字符（有可能为*/?）
                        if(i+1<strlen(reg) && (reg[i+1]=='*' || reg[i+1]=='?')){
                            char ch1[MAXN],ch2[MAXN];
                            memset(ch1,0,sizeof(ch1));
                            memset(ch2,0,sizeof(ch2));
                            tail_string(ch1,reg,i);
                            tail_string(ch2,str,i);
                            return judge(ch1,ch2);
                        }
                        else{
                            return 0;
                        }
                        
                    }
                }
            }
            if(strlen(reg)==strlen(str)){
                // printf("last: run out eq %s %s\n",reg,str);
                return 1;
            }else if(i==strlen(reg)){
                return 0;
            }else{
                // 正则串多了，原字符串用尽。
                // 有两种情况，一种是0匹配问题，这种的特点是第一个符号不是
                if(!validChar(reg[i])){
                    // f?f与f的匹配，即前面那个可能是存在的，也可能是不存在的
                    // Fj? Fj
                    if(reg[i]=='*' || reg[i]=='?'){
                        //枚举两种情况
                        // 前面存在
                        // ?的字符为0
                        char ch1[MAXN],ch2[MAXN];
                        memset(ch1,0,sizeof(ch1));
                        memset(ch2,0,sizeof(ch2));
                        tail_string(ch1,reg,i+1);
                        tail_string(ch2,str,i-1);
                        int result1 = judge(ch1,ch2);
                        if(result1){
                            return 1;
                        }
                        // ?的字符为1
                        memset(ch1,0,sizeof(ch1));
                        memset(ch2,0,sizeof(ch2));
                        tail_string(ch1,reg,i+1);
                        tail_string(ch2,str,i);
                        return judge(ch1,ch2);
                    }else{
                        // f6+与f6的匹配
                        char ch1[MAXN],ch2[MAXN];
                        memset(ch1,0,sizeof(ch1));
                        memset(ch2,0,sizeof(ch2));
                        tail_string(ch1,reg,i+1);
                        tail_string(ch2,str,i);
                        return judge(ch1,ch2);
                    }
                    
                }else{ // 0匹配问题
                    char ch1[MAXN],ch2[MAXN];
                    memset(ch1,0,sizeof(ch1));
                    memset(ch2,0,sizeof(ch2));
                    tail_string(ch1,reg,i);
                    tail_string(ch2,str,i);
                    return judge(ch1,ch2);
                }
            }
        }else{
            // printf("last: first judge %s %s\n",reg,str);
            return 0;
        }
    }else{
        //开始模糊匹配。思路：模糊到精确，然后匹配精确值。
        // 根据给定的数量产生，得到一个ch数组。然后拼接成另外一个数组
        char afterward[MAXN];
        memset(afterward,0,sizeof(afterward));
        // 产生后续数据
        tail_string(afterward,reg,2);// 获得之后的数据结果
        // 比较当前reg是否能完全匹配
        switch(reg[1]){
            case '+':{
                int result = plus_result(afterward,str,reg[0],judge);
                return result;
            }
            case '*':{
                int result = star_result(afterward,str,reg[0],judge);
                return result;
                break;
            }
            case '?':{
                int result = question_result(afterward,str,reg[0],judge);
                return result;
                break;
            }
        }

    }
    return 0;
}

int main(void){
    char reg[MAXN],str[MAXN];
    memset(reg,0,sizeof(reg));
    memset(str,0,sizeof(str));
    // freopen("test.txt","r",stdin);
    // freopen("ans2.txt","w",stdout);
    scanf("%s%s",reg,str);
    printf("%d\n",judge(reg,str));
    return 0;
}