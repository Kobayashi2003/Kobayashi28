#include <stdio.h> 
#include <stdlib.h>

int main() {
    int m=3,n=4;
//    int *q = ...  
    int *q = (int *)malloc(m*n*sizeof(int));
 //   void *t = ..
    void *t = q;
  //  int (*p)[n] = ..
    int (*p)[n] = (int (*)[n])t;

    int i, j;
    for (i=0;i<m*n;i++) 
        q[i] = i+1;
    for (i=0;i<m;i++) {
        for (j=0;j<n;j++)
            printf("%4d",p[i][j]);
        printf("\n");
    }  
    free(q);  
}