#include<stdio.h>
#include<malloc.h>
char data[]="\1\3\5\7";
//通过变换进制进行压缩
void compress()
{
    //首先将data用二进制进行表示
    int *code=NULL;
    int len=0;
    for(int i=0;i<sizeof(data)/sizeof(char)-1;i++)
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
    //然后将代码以16进制的形式进行表示 并且每个数据以8个数字的形式进行表示
    while(len%32)
    {
        len++;
        code=(int *)realloc(code,len*sizeof(int));
        code[len-1]=0;
    }
    for(int i=0;i<len;i++)
    {
        printf("%d",code[i]);
    }
    printf("\n");
    char *p=&data[0];
    for(;p<&data[sizeof(data)/sizeof(char)-1];p+=4)
    {
        int sum=(data[0]<<24)+(data[1]<<16)+(data[2]<<8)+(data[3]);
        int tmp[8]={0},cont=0,ord=0;
        while(sum)
        {
            ord = 0;
            tmp[ord]++;
            sum--;
            while (tmp[ord] - 16 == 0)
            {
                tmp[ord] = 0;
                tmp[++ord]++;
                cont = (ord > cont ? ord : cont);
            }
        }
        for(int i=cont;i>=0;i--)
        {
		    printf("%c",tmp[i]+((tmp[i]>=0&&tmp[i]<=9)?'0':'A'-10));
        }
    }
}
int main()
{
    compress();
    return 0;
}