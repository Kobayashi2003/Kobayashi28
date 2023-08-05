//Antitone
#include<stdio.h>
#define N 100
void Antitone(char *str,int n)
{
    for(int i=0,j=n-1;i<n/2;i++,j--){
        str[i]^=str[j];
        str[j]^=str[i];
        str[i]^=str[j];
    }
}
int main()
{
    char str[N]={'\0'};
    int n;
    for(n=0;(str[n]=getchar())!='\n';n++);
    Antitone(str,n);
    printf("%s\n",str);
    return 0;
}