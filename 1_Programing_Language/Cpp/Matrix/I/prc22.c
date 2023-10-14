#include <stdio.h>
#include <stdlib.h>

void spiralOrder(int **matrix, int m, int n) {
    int count = 0;
    int total = m * n;
    int *result = (int *)malloc(sizeof(int) * total);

    int i = 0, j = 0;

    const int flg = 0x7fffffff;

    while (count < total) {
        while (j < n && matrix[i][j] != flg) {
            result[count++] = matrix[i][j];
            matrix[i][j++] = flg;
        }
        j--;
        i++;
        while (i < m && matrix[i][j] != flg) {
            result[count++] = matrix[i][j];
            matrix[i++][j] = flg;
        }
        i--;
        j--;
        while (j >= 0 && matrix[i][j] != flg) {
            result[count++] = matrix[i][j];
            matrix[i][j--] = flg;
        }
        j++;
        i--;
        while (i >= 0 && matrix[i][j] != flg) {
            result[count++] = matrix[i][j];
            matrix[i--][j] = flg;
        }
        i++;
        j++;
    }

    for (i = 0; i < total; i++) {
        printf("%d ", result[i]);
    }
}


int main()
{
    int m,n,i,j;
    scanf("%d%d",&m,&n);
    int **matrix=(int**)malloc(sizeof(int*)*m); 
    for(i=0; i<m; i++)  
        matrix[i]=(int*)malloc(sizeof(int)*n);
    for(i=0; i<m; i++)  
    {
        for(j=0; j<n; j++)  
        {
            scanf("%d",&matrix[i][j]);     
        }
    }
    spiralOrder(matrix,m,n);
    /*
    for(i=0; i<m; i++)  
    {
        for(j=0; j<n; j++)  
        {
            printf("%d ",matrix[i][j]);
        }
        printf("\n");
    }
    */
    for(i=0; i<m; i++)  
        free(matrix[i]);
 
    free(matrix);
    return 0;
}