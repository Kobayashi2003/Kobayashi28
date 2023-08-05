//换位法

extern void showArray();

void changeSite()
{
	int i,temp,temp1;
	int b[20],max=0;
	int dir[20]={-1,-1,-1,-1,-1,-1};
	for(i=1;i<=n;i++)
		*(b+i)=*(a+i);
	showArray(b);
	while(1){
		max=0;
		b[max]=0;
		//寻找最大的活结点
    	for(i=1;i<=n;i++){
    		if(i+dir[i]>0 && i+dir[i]<=n && b[i]>b[i+dir[i]])
				max=b[i]>b[max]?i:max;
		}
    	if(max==0)
	    	break;
		//交换位置和方向
        temp=b[max];
    	b[max]=b[max+dir[max]];
        b[max+dir[max]]=temp;
		temp1=dir[max+dir[max]];
		dir[max+dir[max]]=dir[max];
        dir[max]=temp1;
		//改变比活结点大的数的方向
    	for(i=1;i<=n;i++)
    		if(b[i]>temp)
	    		dir[i]=-dir[i];
        showArray(b);
	}
}