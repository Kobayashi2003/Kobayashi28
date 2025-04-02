import random
import time

def matrix_multiply(A, B):
    rows_a, cols_a = len(A), len(A[0])
    rows_b, cols_b = len(B), len(B[0])
    if cols_a != rows_b:
        raise ValueError("Invalid matrix dimensions")
    C = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]

    start_time = time.time()
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                C[i][j] += A[i][k] * B[k][j]
    end_time = time.time()
    print(f"Time taken to multiply two matrices: {(end_time - start_time) * 1000} milliseconds.")

    return C

if __name__ == "__main__":
    m = 2000
    k = 200
    n = 1000
    A = [[random.uniform(0.0, 100.0) for _ in range(k)] for _ in range(m)]
    B = [[random.uniform(0.0, 100.0) for _ in range(n)] for _ in range(k)]
    matrix_multiply(A, B)
