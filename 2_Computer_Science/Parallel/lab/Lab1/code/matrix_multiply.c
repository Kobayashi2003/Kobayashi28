#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void initialize_matrix(double *matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i * cols + j] = rand() % 10;
        }
    }
}

void print_matrix(double *matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%.1f ", matrix[i * cols + j]);
        }
        printf("\n");
    }
    printf("\n");
}

int main(int argc, char *argv[]) {
    int rank, size, n;
    double *A = NULL, *B = NULL, *C = NULL;
    double *local_A = NULL, *local_C = NULL;
    double start_time, end_time;
    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    // Matrix size from command line or default to 128
    if (argc > 1) {
        n = atoi(argv[1]);
        if (n < 128 || n > 2048) {
            if (rank == 0) printf("Matrix size should be between 128 and 2048. Using default size 128.\n");
            n = 128;
        }
    } else {
        n = 128;
    }
    
    // Check if n is divisible by size for simplicity
    if (n % size != 0) {
        if (rank == 0) {
            printf("Matrix size (%d) must be divisible by number of processes (%d)\n", n, size);
        }
        MPI_Finalize();
        return 1;
    }
    
    int rows_per_proc = n / size;
    
    // Allocate local portions
    local_A = (double*)malloc(rows_per_proc * n * sizeof(double));
    local_C = (double*)malloc(rows_per_proc * n * sizeof(double));
    memset(local_C, 0, rows_per_proc * n * sizeof(double));
    
    // Master process initializes matrices
    if (rank == 0) {
        A = (double*)malloc(n * n * sizeof(double));
        B = (double*)malloc(n * n * sizeof(double));
        C = (double*)malloc(n * n * sizeof(double));
        
        srand(time(NULL));
        initialize_matrix(A, n, n);
        initialize_matrix(B, n, n);
        
        if (n <= 10) {
            printf("Matrix A:\n");
            print_matrix(A, n, n);
            printf("Matrix B:\n");
            print_matrix(B, n, n);
        }
    }
    
    start_time = MPI_Wtime();
    
    // Distribute matrix A among processes
    MPI_Scatter(A, rows_per_proc * n, MPI_DOUBLE, 
                local_A, rows_per_proc * n, MPI_DOUBLE, 
                0, MPI_COMM_WORLD);
    
    // Broadcast matrix B to all processes
    if (rank == 0) {
        MPI_Bcast(B, n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    } else {
        B = (double*)malloc(n * n * sizeof(double));
        MPI_Bcast(B, n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    }
    
    // Perform local matrix multiplication
    for (int i = 0; i < rows_per_proc; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                local_C[i * n + j] += local_A[i * n + k] * B[k * n + j];
            }
        }
    }
    
    // Gather results back to the root process
    MPI_Gather(local_C, rows_per_proc * n, MPI_DOUBLE,
               C, rows_per_proc * n, MPI_DOUBLE,
               0, MPI_COMM_WORLD);
    
    end_time = MPI_Wtime();
    
    // Print result matrix if small enough
    if (rank == 0) {
        if (n <= 10) {
            printf("Result Matrix C:\n");
            print_matrix(C, n, n);
        }
        printf("Matrix size: %d x %d\n", n, n);
        printf("Number of processes: %d\n", size);
        printf("Execution time: %f seconds\n", end_time - start_time);
    }
    
    // Free memory
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