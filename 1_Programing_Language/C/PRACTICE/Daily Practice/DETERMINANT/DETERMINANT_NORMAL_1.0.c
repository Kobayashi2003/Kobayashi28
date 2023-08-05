#include<stdio.h>

void Output(int str[][10],int n,int result)
{
    printf("Output the determinant\n");
    for(int r=0;r<n;r++)
    {
        for(int c=0;c<n;c++)
            printf("%3d ",str[r][c]);
        putchar('\n');
    }
    printf("The result of the determinant is: %d\n",result);
}

void Seperator(int count,int *num_1000,int *num_100,int *num_10,int *num_1)
{
    *num_1000=count/1000;
    *num_100=(count%1000)/100;
    *num_10=(count%100)/10;
    *num_1=count%10;
}

int Factorial(int n)
{
    int fac=1;
    for(int i=1;i<=n;i++)
        fac*=i;
    return fac;
}

int Pow(int x,int y)
{
    int x_temp=x;
    if(y==0)return 1;
    else for(int i=1;i<y;i++)x*=x_temp;
    return x;
}

int Accumulation(int n)
{
    int sum=0;
    for(int i=1;i<n;i++)
        sum+=i;
    return sum;
}

int Inversion_Number(int *str,int n)
{
    int inv=0;
    for(int i=1;i<=Accumulation(n);i++)
        for(int j=0;j<n-1;j++)
        {
            int temp;
            if(str[j]>str[j+1])
            {
                temp=str[j+1];
                str[j+1]=str[j];
                str[j]=temp;
                inv++;
            }
        }
    return inv;
}

int Result(int sum)
{
    static int temp=0;
    if(sum!=0) 
    temp=sum;
    if(sum==0)
    sum=temp;

    return temp;
}

void Calculate(int det[][10],int trans[][10][10][10][10],int num_1000,int num_100,int num_10,int num_1,int n)
{
    int temp_[10]={0};
    int temp_inv[10]={0};
    int sum=0,temp=1;
    int temp1,temp2,temp3;
    for(int i_1=0;i_1<=num_1000;i_1++)
        {
            if(i_1<num_1000)temp3=9;
            else temp3=num_100;
            for(int i_2=0;i_2<=temp3;i_2++)
            {
                if(i_2<num_100)temp2=9;
                else temp2=num_10;
                for(int i_3=0;i_3<=temp2;i_3++)
                {             
                    if(i_3<num_10)temp1=9;
                    else temp1=num_1;
                    for(int i_4=0;i_4<=temp1;i_4++)
                        for(int i_5=0;i_5<n;i_5++)
                        {
                            temp_inv[i_5]=trans[i_1][i_2][i_3][i_4][i_5]; 
                            temp_[i_5]=det[i_5][trans[i_1][i_2][i_3][i_4][i_5]-1];
                            temp*=temp_[i_5];

                            if(i_5==n-1)
                            {
                                int inv=Inversion_Number(temp_inv,n);
                                printf("inv%d\n",inv);
                                sum+=temp*Pow(-1,inv);
                                printf("sum%d\n",sum);
                                temp=1;
                            }
                        }
                }
            }
        }
    sum=Result(sum);
}

void Transition(int det[][10],int str[],int count,int n)
{
    int num_1000=0,num_100=0,num_10=0,num_1=0;
    int*p_num_1000=&num_1000,*p_num_100=&num_100,*p_num_10=&num_10,*p_num_1=&num_1;
    Seperator(count-1,p_num_1000,p_num_100,p_num_10,p_num_1);

    int trans[10][10][10][10][10];

    for(int i_5=0;i_5<n;i_5++)
        trans[num_1000][num_100][num_10][num_1][i_5]=str[i_5];

    if(count==Factorial(n))
    Calculate(det,trans,num_1000,num_100,num_10,num_1,n);
}

void Permutation(int det[][10],int a[],int n,int k)
{
    static int c[10]={0};
    if(k==0)
        for(int i=0;i<n;i++)c[i]=a[i];
    int b[10]={0};
    for(int i=0;i<k;i++)
        b[i]=a[i];
    b[k]=c[k];

    if(k<n)
    {
        for(int i=0;i<=k;i++)
        {
            int temp=b[i];
            b[i]=b[k];
            b[k]=temp;
            Permutation(det,b,n,k+1);
            temp=b[i];
            b[i]=b[k];
            b[k]=temp;
        }
    }
    if(k==n) 
    {
        static int count=0;

        printf("The %d compose of the array:",count+1);
        for(int i=0;i<n;i++)
            printf("%d",b[i]); 

        Transition(det,b,++count,n);
        
        printf("\n");
    }
}

void Input(int det[][10],int n)
{
    printf("Please int the items of the determinant\n");
    for(int r=0;r<n;r++)
    {
        printf("The %d row:\n",r+1);
        for(int c=0;c<n;c++)
            scanf("%d",&det[r][c]);
    }
    int a[10]={0};
    for(int i=0;i<n;i++)
        a[i]=i+1;

    Permutation(det,a,n,0);
}

int main()
{
    int det[10][10]={{0}};
    int n;
    int result=0;

    printf("Please input the steps of the determinant\n");
    scanf("%d",&n);
    Input(det,n);
    Output(det,n,result=Result(0));
    return 0;
}