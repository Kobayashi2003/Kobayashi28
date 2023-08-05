//翻转法

extern void showArray();

void overturn()
{
    int i,temp,temp1,temp2,j;
    int b[20];
    for(i=1;i<=n;i++) 
        *(b+n-pi+1)=*(a+i);
    showArray(b);
    for(i=1;i<=n;i++)
    {
        //判断第一个数是否为1
        if(i==1&&b[i]!=b[j+i])
        {
            temp=b[i];
            for(j=1;j<n;j++) 
                b[j]=b[j+1];
            b[j]=temp;
            shoeArray(b);
            i=0;
            continue;
        }
        //判断第二个数是否为1
        if(i==2 && b[i]!=i)
        {
			temp1=b[i];
			temp2=b[i-1];
			for(j=1;j+2<=n;j++)
				b[j]=b[j+2];
			b[j]=temp1;
			b[j+1]=temp2;
			showArray(b);
			i=0;
			continue;
		}
        //判断第三个数是否为1
		if(i==3 && b[i]!=i){
			temp=b[i];
			temp1=b[i-1];
			temp2=b[i-2];
			for(j=1;j+3<=n;j++)
				b[j]=b[j+3];
			b[j++]=temp;
			b[j++]=temp1;
			b[j]=temp2;
			showArray(b);
			i=0;
			continue;
		}
    }
}