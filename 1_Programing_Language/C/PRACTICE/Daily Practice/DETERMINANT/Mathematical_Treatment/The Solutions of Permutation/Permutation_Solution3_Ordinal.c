//序数法(排出的序列为有序的)
//str:待排序的字符序列 n:首字符下标 len：字符串长度

extern void showArray();

void ordinal(char * str,int n,int len)
{
	int i;
	char temp;
	if(n==len)
		puts(str);
	for(i=n;i<len;i++){
		temp=str[i];
		str[i]=str[n];
		str[n]=temp;
		ordinal(str,n+1,len);
		temp=str[i];
		str[i]=str[n];
		str[n]=temp;
	}
}