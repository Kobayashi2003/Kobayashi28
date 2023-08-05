//条形码校验
//0 13800 15173 5
//将1、3、5、7、9、11位数字相加得sum1
//将2、4、6、8、10位数字相加得sum2
//9-(sum1*3+sum2-1)%10
#include<stdio.h>
#define UNIVERSAL_PRODUCT_CODE_LEN 12
#define TURE 1
#define FALSE 0
#define CHECK(TOTAL,DIGITAL) ((TOTAL==DIGITAL)?TURE:FALSE)
int main()
{
    int UPC[UNIVERSAL_PRODUCT_CODE_LEN]
        ={0,1,3,8,0,0,1,5,1,7,3,5};
    int sum1=0,sum2=0,total;
    for(int i=1;i<=11;i+=2)
    {
        sum1+=UPC[i-1];
    }
    for(int i=2;i<=10;i+=2)
    {
        sum2+=UPC[i-1];
    }
//    printf("%1d\n",total=9-(sum1*3+sum2-1)%10);
    switch(CHECK(total,UPC[11]))
    {
        case TURE:
        printf("TURE"); break;
        case FALSE:
        printf("FALSE"); break;
    }
    return 0;
}