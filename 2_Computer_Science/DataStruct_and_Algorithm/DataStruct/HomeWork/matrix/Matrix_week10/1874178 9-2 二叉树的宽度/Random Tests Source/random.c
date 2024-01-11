
#include <stdlib.h>

#include <stdio.h>
#include <time.h>

//#define N  50


//generate M permutations of 0,1,...,n-1
int permutation(int n, int M){

  int i;
  int j;
  int x;
  int k;
  int N;
  int l;
  int m;
  time_t t;
  int *A = new int[n+1];
  N = n;

  for (i=0;i<N;i++)
     A[i] = i;

  srand(time(NULL)); 

for (l=0;l<M;l++){
printf("%d\n", N);
  k = N;
  j = 0;
  for (i =0;i<N/2;i++){
    m = rand()%N;    
      x = A[m];
      A[m] = A[k-1];
      A[k-1] = x;
      k = k-1;
  }  
//printf("l:%d\n",l);
  for ( i=0;i<N; i++){
     printf("%d\t", A[i]);
  }
   printf("\n");
}
  delete A;
  return 0;
}

//generate random number of permutation
int main(int argc, char**argv){
//  int A[N];
  int i;
  int j;
  int m;
  int n;
  //int k;
  int case_num;
  time_t t;
  srand(time(NULL));
  case_num = rand()%10+10;
 // int *B = malloc(n*sizeof(int));
  
  n = random()%20 + 10;
  printf("%d\n", case_num);
  
  permutation(n, case_num);
  

  return 0;
}

