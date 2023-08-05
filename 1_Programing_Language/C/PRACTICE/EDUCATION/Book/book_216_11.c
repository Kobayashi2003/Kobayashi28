#include<stdio.h>
#include<string.h>
void Bubble_Sort(char *str,int end)
{
    if(end!=0){
        for(int i=0;i<end;i++){
            if(str[i]>str[i+1]){
                str[i]^=str[i+1];
                str[i+1]^=str[i];
                str[i]^=str[i+1];
            }
        }
        Bubble_Sort(str,--end);
    }
}
int main()
{
    char str[10]="9876543210";
    Bubble_Sort(str,9);
    puts(str);
    return 0;
}