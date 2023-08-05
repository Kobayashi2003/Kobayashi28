//设要排序的数组是A[0]……A[N-1]，首先任意选取一个数据（通常选用数组的第一个数）作为关键数据，然后将所有比它小的数都放到它左边，所有比它大的数都放到它右边，这个过程称为一趟快速排序。值得注意的是，快速排序不是一种稳定的排序算法，也就是说，多个相同的值的相对位置也许会在算法结束时产生变动。

/*一趟快速排序的算法是：
1）设置两个变量i、j，排序开始的时候：i=0，j=N-1；
2）以第一个数组元素作为关键数据，赋值给key，即key=A[0]；
3）从j开始向前搜索，即由后开始向前搜索(j--)，找到第一个小于key的值A[j]，将A[j]和A[i]的值交换；
4）从i开始向后搜索，即由前开始向后搜索(i++)，找到第一个大于key的A[i]，将A[i]和A[j]的值交换；
5）重复第3、4步，直到i==j； (3,4步中，没找到符合条件的值，即3中A[j]不小于key,4中A[i]不大于key的时候改变j、i的值，使得j=j-1，i=i+1，直至找到为止。找到符合条件的值，进行交换的时候i， j指针位置不变。另外，i==j这一过程一定正好是i+或j-完成的时候，此时令循环结束）。
*/

/*排序演示
假设一开始序列{xi}是：5，3，7，6，4，1，0，2，9，10，8。
此时，ref=5，i=1，j=11，从后往前找，第一个比5小的数是x8=2，因此序列为：2，3，7，6，4，1，0，5，9，10，8。
此时i=1，j=8，从前往后找，第一个比5大的数是x3=7，因此序列为：2，3，5，6，4，1，0，7，9，10，8。
此时，i=3，j=8，从第8位往前找，第一个比5小的数是x7=0，因此：2，3，0，6，4，1，5，7，9，10，8。
此时，i=3，j=7，从第3位往后找，第一个比5大的数是x4=6，因此：2，3，0，5，4，1，6，7，9，10，8。
此时，i=4，j=7，从第7位往前找，第一个比5小的数是x6=1，因此：2，3，0，1，4，5，6，7，9，10，8。
此时，i=4，j=6，从第4位往后找，直到第6位才有比5大的数，这时，i=j=6，ref成为一条分界线，它之前的数都比它小，之后的数都比它大，对于前后两部分数，可以采用同样的方法来排序
*/

#include<stdio.h>
void Input(int *array,int *ori)
{
    for(int i=0;i<10;i++)
    {
        scanf("%d",&array[i]);
        ori[i]=array[i];
    }
}
void Output(int *array)
{
    for(int i=0;i<10;i++)
        printf("%d ",array[i]);
    putchar('\n');
}
void Quick_Sort(int *array,int *ori,int count)
{
    int key=ori[count];
    int l,s,n;
    for(int i=0;i<10;i++)
        if(array[i]==key)
            {
                n=l=s=i;
                break;
            }
    for(int i=n;i>=0;i--)
        if(array[i]>key)
        {
            l=i;
            break;
        }
    for(int i=n;i<10;i++)
        if(array[i]<key)
        {
            s=i;
            break;
        }
    if(l<s)
    {
        int temp=array[s];
        array[s]=array[l];
        array[l]=temp;
        Output(array);
        Quick_Sort(array,ori,count);
    }
    else if(l==s&&count!=9) Quick_Sort(array,ori,++count);
}
int main()
{
    int array[10],ori[10];
    Input(array,ori);
    Quick_Sort(array,ori,0);
    Output(array);
    return 0;
}