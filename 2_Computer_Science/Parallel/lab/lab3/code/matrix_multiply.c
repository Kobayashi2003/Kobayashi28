#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define THREAD_NUM 16
#define MATRIX_SIZE 2048

typedef struct {
    int thread_id;
    int start_row;
    int end_row;
    int N;
    double** A;
    double** B;
    double** C;
} ThreadData;

void* matrix_multiply(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    for (int i = data->start_row; i < data->end_row; i++) {
        for (int j = 0; j < data->N; j++) {
            for (int k = 0; k < data->N; k++) {
                data->C[i][j] += data->A[i][k] * data->B[k][j];
            }
        }
    }
    return NULL;
}

void print_matrix(double** matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%f ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {

    ThreadData thread_data[THREAD_NUM];
    pthread_t threads[THREAD_NUM];

    double** A = (double**)malloc(MATRIX_SIZE * sizeof(double*));
    double** B = (double**)malloc(MATRIX_SIZE * sizeof(double*));
    double** C = (double**)malloc(MATRIX_SIZE * sizeof(double*));
    for (int i = 0; i < MATRIX_SIZE; i++) {
        A[i] = (double*)malloc(MATRIX_SIZE * sizeof(double));
        B[i] = (double*)malloc(MATRIX_SIZE * sizeof(double));
        C[i] = (double*)malloc(MATRIX_SIZE * sizeof(double));
    }
    for (int i = 0; i < MATRIX_SIZE; i++) {
        for (int j = 0; j < MATRIX_SIZE; j++) {
            A[i][j] = i + j;
            B[i][j] = i + j;
        }
    }

    clock_t start_time = clock();

    int row_per_thread = MATRIX_SIZE / THREAD_NUM;
    for (int i = 0; i < THREAD_NUM; i++) {
        thread_data[i].thread_id = i;
        thread_data[i].start_row = i * row_per_thread;
        // thread_data[i].end_row = (i + 1) * row_per_thread;
        thread_data[i].end_row = i == THREAD_NUM - 1 ? MATRIX_SIZE : (i + 1) * row_per_thread;
        thread_data[i].N = MATRIX_SIZE;
        thread_data[i].A = A;
        thread_data[i].B = B;
        thread_data[i].C = C;
        pthread_create(&threads[i], NULL, matrix_multiply, &thread_data[i]);
    }

    for (int i = 0; i < THREAD_NUM; i++) {
        pthread_join(threads[i], NULL);
    }

    clock_t end_time = clock();
    printf("Matrix size: %d x %d\n", MATRIX_SIZE, MATRIX_SIZE);
    printf("Number of threads: %d\n", THREAD_NUM);
    printf("Time taken: %f seconds\n", (double)(end_time - start_time) / CLOCKS_PER_SEC);
    FILE* file = fopen("matrix_multiply_results.txt", "a");
    fprintf(file, "Matrix size: %d x %d\n", MATRIX_SIZE, MATRIX_SIZE);
    fprintf(file, "Number of threads: %d\n", THREAD_NUM);
    fprintf(file, "Time taken: %f seconds\n\n", (double)(end_time - start_time) / CLOCKS_PER_SEC);
    fclose(file);

    // print_matrix(A, MATRIX_SIZE, MATRIX_SIZE);
    // print_matrix(B, MATRIX_SIZE, MATRIX_SIZE);
    // print_matrix(C, MATRIX_SIZE, MATRIX_SIZE);

    for (int i = 0; i < MATRIX_SIZE; i++) {
        free(A[i]);
        free(B[i]);
        free(C[i]);
    }
    free(A);
    free(B);
    free(C);

    return 0;
}
