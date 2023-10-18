void swap(int* p, int* q);

void print_array(int* p, int size);

void print_matrix(int** mat, int row, int col);


void swap(int *p, int *q) {
    int temp = *p;
    *p = *q;
    *q = temp;
}

void print_array(int *p, int size) {
    for (int i = 0; i < size; ++i) {
        printf("%d\n", p[i]);
    }
    printf("\n");   
}

void print_matrix(int **mat, int row, int col) {
    for (int i = 0; i < row; ++i) {
        for (int j = 0; j < col; j++) {
            printf("%d ", mat[i][j]);
        }
        printf("\n");
    }
}