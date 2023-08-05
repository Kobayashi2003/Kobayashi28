#include<stdio.h>
int main()
{
    typedef enum Color{red,yellow,blue,whote,black}Color;
    enum Color i,j,k,pri;
    int n,loop;
    n=0;
    for(i=red;i<=black;i=(Color)(i+1))
        for(j=red;j<=black;j++)
            if(i!=j)
            {
                for(k=red;k<=black;k++)
                    if((k!=i)&&(k!=j))
                    {
                        n++;
                        printf("%-4d",n);
                        for(loop=1;loop<=3;loop++)
                        {
                           switch(loop)
                           {
                               case 1:pri=i;break;
                               case 2:pri=j;break;
                               case 3:pri=k;break;
                               default:break;
                           } 
                           switch(pri)
                           {
                               case red:printf("%-10s","red");break;
                               case yellow:printf("%-10s","yellow");break;
                               case blue:printf("%-10s","blue");break;
                               case black:printf("%-10s","black");break;
                               default:break;
                           }
                        }
                        printf("\n");
                    }
            }
    printf("\ntatal:%5d\n",n);
    return 0;
}