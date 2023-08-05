#include<stdio.h>
#include<string.h>
#define N 10
#define MARK 1
#define BLANK 0
typedef enum State{OFF,ON}State;
void selectArray(char *str,int len)
{
    State On_Off=OFF;
    char Save[N][N]={'\0'};
    char visual[N]={'\0'};
    int number=0,count=0;
    for(int i=0;i<len;i++)
        if(str[i]>='0'&&str[i]<='9')visual[i]=MARK;
    for(int i=0;i<len;i++)
    {
        if(visual[i]==MARK)
        {
            if(On_Off==OFF)count=0;
            On_Off=ON;
        }
        if(visual[i]==BLANK)
        {
            if(On_Off==ON)number++;
            On_Off=OFF;
        }
        switch(On_Off)
        {
            case ON:
            Save[number][count]=str[i];
            count++;
            break;

            case OFF:
            break;
        }
    }
    for(int i=0;i<=number;i++,putchar('\n'))
        for(int j=0;j<N;j++)
            printf("%c",Save[i][j]);
    putchar('\n');
}
int main()
{
    char str[N]={'\0'};
    printf("Please enter a string:\n");
    scanf("%s",str);
    selectArray(str,strlen(str));
    return 0;
}
