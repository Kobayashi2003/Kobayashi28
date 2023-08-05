#include<stdio.h>
int main()
{
 int a,b,c,d,e,f,g,h,num;
 scanf("%d",&f);
 if(f%10000!=f)
    num=5;
 else if(f%1000!=f)
    num=4;
 else if(f%100!=f)
    num=3;
 else if(f%10!=f)
    num=2;
 else
    num=1;
 printf("num=%d\n",num);
 a=f/10000;
 b=(f%10000)/1000;
 c=(f%1000)/100;
 d=(f%100)/10;
 e=f%10;
 printf("%d\n%d\n%d\n%d\n%d\n",a,b,c,d,e);
 {if(num==5)
  printf("%d%d%d%d%d",e,d,c,b,a);
 else if(num==4)
  printf("%d%d%d%d",e,d,c,b);
 else if(num=3)
  printf("%d%d%d",e,d,c);
 else if(num==2)
     printf("%d%d",e,d);
 else if(num==1)
  printf("%d",e);
 }
 return 0;
}