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
    
    // Allocate memory for local matrices
    local_A = (double*)malloc(rows_per_proc * n * sizeof(double));
    local_C = (double*)malloc(rows_per_proc * n * sizeof(double));
    memset(local_C, 0, rows_per_proc * n * sizeof(double));
    
    // Root process initializes matrices
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
    
    // Distribute matrix A using point-to-point communication
    if (rank == 0) {
        // Root process sends parts of A to other processes
        for (int dest = 1; dest < size; dest++) {
            MPI_Send(A + dest * rows_per_proc * n, 
                    rows_per_proc * n, 
                    MPI_DOUBLE, 
                    dest, 
                    0, 
                    MPI_COMM_WORLD);
        }
        // Root process keeps its own part
        memcpy(local_A, A, rows_per_proc * n * sizeof(double));
    } else {
        // Other processes receive their part of A
        MPI_Recv(local_A, 
                rows_per_proc * n, 
                MPI_DOUBLE, 
                0, 
                0, 
                MPI_COMM_WORLD, 
                MPI_STATUS_IGNORE);
    }
    
    // Distribute matrix B using point-to-point communication
    if (rank == 0) {
        // Root process sends B to all other processes
        for (int dest = 1; dest < size; dest++) {
            MPI_Send(B, 
                    n * n, 
                    MPI_DOUBLE, 
                    dest, 
                    1, 
                    MPI_COMM_WORLD);
        }
    } else {
        // Other processes allocate memory for B and receive it
        B = (double*)malloc(n * n * sizeof(double));
        MPI_Recv(B, 
                n * n, 
                MPI_DOUBLE, 
                0, 
                1, 
                MPI_COMM_WORLD, 
                MPI_STATUS_IGNORE);
    }
    
    // Perform local matrix multiplication
    for (int i = 0; i < rows_per_proc; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                local_C[i * n + j] += local_A[i * n + k] * B[k * n + j];
            }
        }
    }
    
    // Gather results using point-to-point communication
    if (rank == 0) {
        // Root process receives results from other processes
        for (int src = 1; src < size; src++) {
            MPI_Recv(C + src * rows_per_proc * n, 
                    rows_per_proc * n, 
                    MPI_DOUBLE, 
                    src, 
                    2, 
                    MPI_COMM_WORLD, 
                    MPI_STATUS_IGNORE);
        }
        // Root process copies its own result
        memcpy(C, local_C, rows_per_proc * n * sizeof(double));
    } else {
        // Other processes send their results to root
        MPI_Send(local_C, 
                rows_per_proc * n, 
                MPI_DOUBLE, 
                0, 
                2, 
                MPI_COMM_WORLD);
    }
    
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