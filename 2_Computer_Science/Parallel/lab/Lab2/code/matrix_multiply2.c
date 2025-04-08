#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

typedef struct {
    int row_index;
    int row_size;
    double row_data[];
} MatrixRow;

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
    double *local_C = NULL;
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
    
    MPI_Datatype matrix_row_type;
    int blocklengths[3] = {1, 1, n};
    MPI_Aint displacements[3];
    MPI_Datatype types[3] = {MPI_INT, MPI_INT, MPI_DOUBLE};
    
    MatrixRow *dummy = NULL;
    MPI_Aint base_address;
    MPI_Get_address(dummy, &base_address);
    MPI_Get_address(&dummy->row_index, &displacements[0]);
    MPI_Get_address(&dummy->row_size, &displacements[1]);
    MPI_Get_address(&dummy->row_data, &displacements[2]);
    
    displacements[0] = MPI_Aint_diff(displacements[0], base_address);
    displacements[1] = MPI_Aint_diff(displacements[1], base_address);
    displacements[2] = MPI_Aint_diff(displacements[2], base_address);
    
    MPI_Type_create_struct(3, blocklengths, displacements, types, &matrix_row_type);
    MPI_Type_commit(&matrix_row_type);
    
    MatrixRow *send_buffer = (MatrixRow*)malloc(size * (sizeof(MatrixRow) + n * sizeof(double)));
    MatrixRow *recv_buffer = (MatrixRow*)malloc(rows_per_proc * (sizeof(MatrixRow) + n * sizeof(double)));
    local_C = (double*)malloc(rows_per_proc * n * sizeof(double));
    memset(local_C, 0, rows_per_proc * n * sizeof(double));
    
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
        
        for (int proc = 0; proc < size; proc++) {
            for (int i = 0; i < rows_per_proc; i++) {
                int row_idx = proc * rows_per_proc + i;
                MatrixRow *row = (MatrixRow*)((char*)send_buffer + proc * (sizeof(MatrixRow) + n * sizeof(double)));
                row->row_index = row_idx;
                row->row_size = n;
                memcpy(row->row_data, &A[row_idx * n], n * sizeof(double));
            }
        }
    } else {
        B = (double*)malloc(n * n * sizeof(double));
    }
    
    start_time = MPI_Wtime();
    
    MPI_Bcast(B, n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    int *sendcounts = (int*)malloc(size * sizeof(int));
    int *displs = (int*)malloc(size * sizeof(int));
    for (int i = 0; i < size; i++) {
        sendcounts[i] = 1;
        displs[i] = i;
    }
    
    MPI_Scatterv(send_buffer, sendcounts, displs, matrix_row_type,
                 recv_buffer, rows_per_proc, matrix_row_type,
                 0, MPI_COMM_WORLD);
    
    for (int i = 0; i < rows_per_proc; i++) {
        MatrixRow *row = (MatrixRow*)((char*)recv_buffer + i * (sizeof(MatrixRow) + n * sizeof(double)));
        for (int j = 0; j < n; j++) {
            local_C[i * n + j] = 0;
            for (int k = 0; k < n; k++) {
                local_C[i * n + j] += row->row_data[k] * B[k * n + j];
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
        free(sendcounts);
        free(displs);
    }
    free(B);
    free(send_buffer);
    free(recv_buffer);
    free(local_C);
    MPI_Type_free(&matrix_row_type);
    
    MPI_Finalize();
    return 0;
}
