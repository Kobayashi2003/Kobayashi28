//分子：numerator，分母：denominator，公因数：diviser 分数：fraction
//现更新至分数的加减
#include<stdio.h>
#include<string.h>
#define N 100

int Pow(int num,int n)
{
    if(n==0)num=1;
    else if(n>0)
    for(int i=1;i<n;i++)num*=num;
    return num;
}

void Cut(char *str,int n)
{
    char temp[N-1]={'\0'};
    for(int i=0,j=0;i<N;i++,j++)
    {
        if(i==n)i++;
        temp[j]=str[i];
    }
    memset(str,'\0',N);
    strcpy(str,temp);
}

int SignOff(char *frac)
{
    int sign=0;
    for(int i=0;i<N;i++)
        if(frac[i]=='-')
        {
            Cut(frac,i);
            sign++;
        }
    return sign;
}

void Reduction(int num,int den)
{
    for(int div=1;div<=num&&div<=den;div++)
        if((num%div==0)&&(den%div==0)&&(div!=1))
        {
            num/=div;
            den/=div;
            div=1;
        }
    printf("The result is:");
    if(num==den)printf("1\n");
    else if(den==1)printf("%d\n",num);
    else if(num==0)printf("0\n");
    else printf("%d/%d\n",num,den);
}

void Change(char *frac,int *num,int *den)
{
    int sign=SignOff(frac);
    int count_num,count_den;
    for(count_num=0;(frac[count_num]!='/')&&(frac[count_num]!='\0');count_num++);
    for(count_den=0;frac[count_den+count_num+1]!='\0';count_den++);

    for(int i=count_num+1;count_den>0;count_den--,i++)
        *den+=(frac[i]-'0')*Pow(10,count_den-1);
    for(int i=0;count_num>0;count_num--,i++)
        *num+=(frac[i]-'0')*Pow(10,count_num-1);
    *num*=Pow(-1,sign);
}

void CalculateFraction(int num_1,int den_1,int num_2,int den_2)
{
    int num_3,den_3;

    if(den_1==0)den_1=1;
    if(den_2==0)den_2=1;

    num_3=num_1*den_2+num_2*den_1;
    den_3=den_1*den_2;
    printf("%d/%d\n",num_3,den_3);

    Reduction(num_3,den_3);
}

int main()
{
    char *Format="%d/%d %d/%d\n";
    char frac_1[N]={'\0'},frac_2[N]={'\0'};
    int num_1=0,den_1=0,num_2=0,den_2=0;
    int *p_num_1=&num_1,*p_num_2=&num_2,*p_den_1=&den_1,*p_den_2=&den_2;

    printf("Please enter the first frac:\n");
    gets(frac_1);
    Change(frac_1,p_num_1,p_den_1);

    printf("Please enter the second frac\n");
    gets(frac_2);
    Change(frac_2,p_num_2,p_den_2);
    
    printf(Format,num_1,den_1,num_2,den_2);

    CalculateFraction(num_1,den_1,num_2,den_2);

    return 0;
}