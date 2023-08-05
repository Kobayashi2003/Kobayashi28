#include<stdio.h>
#include<math.h>
int main()
{
    int num ;
    printf("Please input an integer number:");
    scanf("%d", &num);
    int i;
    for(i=0;!((int)pow(10,i)<=num&&num<(int)pow(10,i+1));i++){
        //blank
    };
    printf("num^2=%d\n",(int)pow(num,2));
    if(((int)pow(num,2))%((int)pow(10,i+1))==num)
    {
        printf("TRUE\n");
        return 0;
    }
    printf("FALSE\n");
    return 0;
}