#include<stdio.h>
#include<assert.h>

int cmp_inc(int a,int b);
int cmp_desc(int a,int b);

void SelectedSortInt(int *nums, int n, int (*fcmp)(int,int)) {
    for (int i=0; i<=n-2; i++) {
        //find minimum idx
        int idx = i;
        int min = nums[i];
        for (int j=i+1; j<=n-1; j++) {
            if (fcmp(nums[j],min) < 0) {
                idx = j;
                min = nums[j];
            }
        }
        
        //swap
        if (i!=idx) {
            int temp = nums[i];
            nums[i] = nums[idx];
            nums[idx] = temp;
        }
    }
}

int cmp_inc(int a,int b) {
    return a-b; 
}

int cmp_desc(int a,int b) {
    return -(a-b); 
}

int main() {
	int a[10] = {1,3,7,2,6,8,10,15,9,18};
	int expected[10] = {1,2,3,6,7,8,9,10,15,18};

    int n = sizeof(a)/sizeof(int);
	SelectedSortInt(a,n,cmp_inc);
	for (int i=0;i<n;i++) 
	    //assert(a[i]==expected[i]);
	    printf("%4d",a[i]);
	    
	return 0; 
}