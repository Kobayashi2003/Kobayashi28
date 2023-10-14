#include <stdio.h>
#include <stdlib.h>

int gcd_recursive(int a,int b){
	printf("call: gcd_recursive(%d,%d)\n",a,b);
    if(b==0){
        printf("gcd_recursive(%d,%d) return:%d\n",a,b,a);
        return a;
    }
    int res = gcd_recursive(b,a%b);
	printf("gcd_recursive(%d,%d) return:%d\n",a,b,res);
	return res;
}
int gcd_loop(int a,int b){
	while (b!=0){
        int t = a%b;
        a = b;
        b = t;
		printf("loop:(%d,%d)\n",a,b);
	}
    return a;
}

int main(int argc, char *argv[]) {
	int a,b;
	scanf("%d %d",&a,&b);
	gcd_loop(a,b);
	gcd_recursive(a,b);
	return 0;
}