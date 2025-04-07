#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

typedef struct {
    int rows;
    int cols;
    double *data;
} Matrix;

void initialize_matrix(Matrix *matrix, int rows, int cols) {
    matrix->rows = rows;
    matrix->cols = cols;
    matrix->data = (double*)malloc(rows * cols * sizeof(double));
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix->data[i * cols + j] = rand() % 10;
        }
    }
}

void print_matrix(Matrix *matrix) {
    for (int i = 0; i < matrix->rows; i++) {
        for (int j = 0; j < matrix->cols; j++) {
            printf("%.1f ", matrix->data[i * matrix->cols + j]);
        }
        printf("\n");
    }
    printf("\n");
}

void free_matrix(Matrix *matrix) {
    if (matrix->data != NULL) {
        free(matrix->data);
        matrix->data = NULL;
    }
}

int main(int argc, char *argv[]) {
    int n = 128;
    int rank, size;
    Matrix A, B, C;
    Matrix local_A, local_C;
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
    
    MPI_Datatype matrix_type;
    int blocklengths[3] = {1, 1, rows_per_proc * n};
    MPI_Aint displacements[3];
    MPI_Datatype types[3] = {MPI_INT, MPI_INT, MPI_DOUBLE};
    
    Matrix temp;
    MPI_Aint base_address;
    MPI_Get_address(&temp, &base_address);
    MPI_Get_address(&temp.rows, &displacements[0]);
    MPI_Get_address(&temp.cols, &displacements[1]);
    MPI_Get_address(&temp.data, &displacements[2]);
    
    for (int i = 0; i < 3; i++) {
        displacements[i] = MPI_Aint_diff(displacements[i], base_address);
    }
    
    MPI_Type_create_struct(3, blocklengths, displacements, types, &matrix_type);
    MPI_Type_commit(&matrix_type);
    
    if (rank == 0) {
        initialize_matrix(&A, n, n);
        initialize_matrix(&B, n, n);
        C.rows = n;
        C.cols = n;
        C.data = (double*)malloc(n * n * sizeof(double));
        
        if (n <= 10) {
            printf("Matrix A:\n");
            print_matrix(&A);
            printf("Matrix B:\n");
            print_matrix(&B);
        }
    }
    
    local_A.rows = rows_per_proc;
    local_A.cols = n;
    local_A.data = (double*)malloc(rows_per_proc * n * sizeof(double));
    
    local_C.rows = rows_per_proc;
    local_C.cols = n;
    local_C.data = (double*)malloc(rows_per_proc * n * sizeof(double));
    memset(local_C.data, 0, rows_per_proc * n * sizeof(double));
    
    start_time = MPI_Wtime();
    
    if (rank == 0) {
        for (int dest = 1; dest < size; dest++) {
            Matrix send_A;
            send_A.rows = rows_per_proc;
            send_A.cols = n;
            send_A.data = A.data + dest * rows_per_proc * n;
            MPI_Send(&send_A, 1, matrix_type, dest, 0, MPI_COMM_WORLD);
        }
        memcpy(local_A.data, A.data, rows_per_proc * n * sizeof(double));
    } else {
        MPI_Recv(&local_A, 1, matrix_type, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
    
    if (rank == 0) {
        for (int dest = 1; dest < size; dest++) {
            MPI_Send(&B, 1, matrix_type, dest, 1, MPI_COMM_WORLD);
        }
    } else {
        MPI_Recv(&B, 1, matrix_type, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
    
    for (int i = 0; i < rows_per_proc; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                local_C.data[i * n + j] += local_A.data[i * n + k] * B.data[k * n + j];
            }
        }
    }
    
    if (rank == 0) {
        for (int src = 1; src < size; src++) {
            Matrix recv_C;
            recv_C.rows = rows_per_proc;
            recv_C.cols = n;
            recv_C.data = C.data + src * rows_per_proc * n;
            MPI_Recv(&recv_C, 1, matrix_type, src, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
        memcpy(C.data, local_C.data, rows_per_proc * n * sizeof(double));
    } else {
        MPI_Send(&local_C, 1, matrix_type, 0, 2, MPI_COMM_WORLD);
    }
    
    end_time = MPI_Wtime();
    
    if (rank == 0) {
        if (n <= 10) {
            printf("Result Matrix C:\n");
            print_matrix(&C);
        }
        printf("Matrix size: %d x %d\n", n, n);
        printf("Number of processes: %d\n", size);
        printf("Execution time: %f seconds\n", end_time - start_time);
    }
    
    if (rank == 0) {
        free_matrix(&A);
        free_matrix(&C);
    }
    free_matrix(&B);
    free_matrix(&local_A);
    free_matrix(&local_C);
    MPI_Type_free(&matrix_type);
    
    MPI_Finalize();
    return 0;
}