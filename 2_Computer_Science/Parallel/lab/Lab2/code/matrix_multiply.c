#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void initialize_matrix(double *matrix, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            matrix[i * n + j] = rand() % 10;
        }
    }
}

void print_matrix(double *matrix, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%.1f ", matrix[i * n + j]);
        }
        printf("\n");
    }
    printf("\n");
}

int main(int argc, char *argv[]) {
    int n = 128;
    int rank, size;
    double *A = NULL, *B = NULL, *C = NULL;
    double *local_A = NULL, *local_C = NULL;
    double start_time, end_time;
    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    if (n % size != 0) {
        if (rank == 0) {
            printf("Matrix size (%d) must be divisible by number of processes (%d)\n", n, size);
        }
        MPI_Finalize();
        return 1;
    }
    
    int rows_per_proc = n / size;
    
    if (rank == 0) {
        A = (double*)malloc(n * n * sizeof(double));
        B = (double*)malloc(n * n * sizeof(double));
        C = (double*)malloc(n * n * sizeof(double));
        
        srand(time(NULL));
        initialize_matrix(A, n);
        initialize_matrix(B, n);
        
        if (n <= 10) {
            printf("Matrix A:\n");
            print_matrix(A, n);
            printf("Matrix B:\n");
            print_matrix(B, n);
        }
    } else {
        B = (double*)malloc(n * n * sizeof(double));
    }
    
    local_A = (double*)malloc(rows_per_proc * n * sizeof(double));
    local_C = (double*)malloc(rows_per_proc * n * sizeof(double));
    memset(local_C, 0, rows_per_proc * n * sizeof(double));
    
    start_time = MPI_Wtime();
    
    MPI_Bcast(B, n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    MPI_Scatter(A, rows_per_proc * n, MPI_DOUBLE,
                local_A, rows_per_proc * n, MPI_DOUBLE,
                0, MPI_COMM_WORLD);
    
    for (int i = 0; i < rows_per_proc; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                local_C[i * n + j] += local_A[i * n + k] * B[k * n + j];
            }
        }
    }
    
    MPI_Gather(local_C, rows_per_proc * n, MPI_DOUBLE,
               C, rows_per_proc * n, MPI_DOUBLE,
               0, MPI_COMM_WORLD);
    
    end_time = MPI_Wtime();
    
    if (rank == 0) {
        if (n <= 10) {
            printf("Result Matrix C:\n");
            print_matrix(C, n);
        }
        printf("Matrix size: %d x %d\n", n, n);
        printf("Number of processes: %d\n", size);
        printf("Execution time: %f seconds\n", end_time - start_time);
    }
    
    if (rank == 0) {
        free(A);
        free(C);
    }
    free(B);
    free(local_A);
    free(local_C);
    
    MPI_Finalize();
    return 0;
}