//https://blog.csdn.net/weixin_39970668/article/details/110582862?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_aa&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_aa&utm_relevant_index=2

//base64的加密及解密 完成于2022/2/18

//修复了在解密过程中无法正常显示大写字母C的BUG 完成于2022/6/1

#include<stdio.h>
#include<malloc.h>
#include<math.h>
//将8bit用6bit表示
//A-Z 0-25 a-z 26-51 0-9 52-61 + 62 / 63
char TABLE[64]={'\0'};

char data[] = "I love Garw Gura!";
// char CODE[] = "SSBsb3ZlIEdhcncgR3VyYSE==";

char CODE[] = "NzI2OTEwOTkz";
//base64编码：1、将data转换为二进制进行表示 2、将转换后的二进制代码以每6bit为一份的形式进行分割，若最后一组不足6bit，则将其用0补齐 3、把每一组的二进制码转换为十进制，并通过查表找到该数所对应的base64字符 4、最后在得到的base64编码的末尾加上"==""

void makeTable(void)
{
    TABLE[0] = 'A';
    for (int i = 1; i < 26; i++)
    {
        TABLE[i] = TABLE[i - 1] + 1;
    }
    TABLE[26] = 'a';
    for (int i = 27; i < 52; i++)
    {
        TABLE[i] = TABLE[i - 1] + 1;
    }
    TABLE[52] = '0';
    for (int i = 53; i < 62; i++)
    {
        TABLE[i] = TABLE[i - 1] + 1;
    }
    TABLE[62] = '+';
    TABLE[63] = '/';
}

void BASE64_ENCODE()
{
    if(data[0]=='\0') return;
    int *code=NULL;
    int len=0;
    for(unsigned long long int i=0;i<sizeof(data)/sizeof(char)-1;i++)
    {
        int tmp[8]={0},cont=0,ord=0;
        int num=(int)data[i];
        while(num)
        {
            ord = 0;
            tmp[ord]++;
            num--;
            while (tmp[ord] - 2 == 0)
            {
                tmp[ord] = 0;
                tmp[++ord]++;
                cont = (ord > cont ? ord : cont);
            }
        }
        for(int i=7;i>=0;i--)
        {
            if(len==0)
            {
                len++;
                code=(int *)malloc(sizeof(int));
                code[0]=tmp[7];
            }
            else
            {
                len++;
                code=(int *)realloc(code,sizeof(int)*len);
                code[len-1]=tmp[i];
            }
        }
    }
    while(len%6)
    {
        len++;
        code=(int *)realloc(code,len*sizeof(int));
        code[len-1]=0;
    }
    printf("The base64 code is:\n");
    for(int i=5;i<len;i+=6)
    {
        int sum=0;
        for(int j=0;j<6;j++)
        {
            if(code[i-j]==1)
                sum+=(int)pow(2.0,(double)j);
        }
        printf("%c",TABLE[sum]);
    }
    printf("==");
    printf("\n");
}

//base64解码 1、将code对照base64编码表转换为二进制进行表示 2、将转换后的二进制代码以每8bit为一份的形式进行分割，若最后一组不足8bit，则将其舍去 3、把每一组的二进制编码转换为十进制，并通过查找ASCII码输出对应的字符

void BASE64_DECODE()
{
    if(CODE[0]=='\0') return;
    int *code=NULL,len=0;
    for(unsigned long long int i=0;i<sizeof(CODE)/sizeof(char)-1&&CODE[i]!='=';i++)
    {
        int num=0;
        if(CODE[i]>='A'&&CODE[i]<='Z')
            num=CODE[i]-'A';
        else if(CODE[i]>='a'&&CODE[i]<='z')
            num=CODE[i]-'a'+26;
        else if(CODE[i]>='0'&&CODE[i]<='9')
            num=CODE[i]-'0'+52;
        else if(CODE[i]=='+')
            num=62;
        else if(CODE[i]=='/')
            num=63;
        else
        {
            printf("WRONG CODE!!\n");
            return ;
        }
        int tmp[6] = {0}, cont = 0, ord = 0;
        while (num)
        {
            ord = 0;
            tmp[ord]++;
            num--;
            while (tmp[ord] - 2 == 0)
            {
                tmp[ord] = 0;
                tmp[++ord]++;
                cont = (ord > cont ? ord : cont);
            }
        }
        for(int i=5;i>=0;i--)
        {
            if(len==0)
            {
                len++;
                code=(int *)malloc(sizeof(int));
                code[0]=tmp[6];
            }
            else
            {
                len++;
                code=(int *)realloc(code,sizeof(int)*len);
                code[len-1]=tmp[i];
            }
        }
    }
        for(int *p=code;p<code+len;p+=8)
        {
            int sum=0;
            for(int i=0;i<8;i++)
            {
                sum<<=1;
                sum+=p[i];
            }
            printf("%c",(char)sum);
        }
}

int main()
{
    makeTable();

    int model = 0;
    printf("Please choose the model:\n");
    printf("MODEL1:ENCODE MODEL2:DECODE\n");
    printf("The model you want to use: ");
    scanf("%d",&model);
    switch(model)
    {
        case 1:
        BASE64_ENCODE();
        break;
        case 2:
        BASE64_DECODE();
        break;
        default:
        printf("WRONG!");
    }
    return 0;
}