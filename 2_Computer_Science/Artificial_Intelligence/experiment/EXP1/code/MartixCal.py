def MatrixAdd(A, B):
    """
    :param A: list[lsit[int]]
    :param B: list[lsit[int]]
    :return:  list[list[int]]
    """
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def MatrixMul(A, B):
    """
    :param A: list[lsit[int]]
    :param B: list[lsit[int]]
    :return:  list[list[int]]
    """
    return [[sum(A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))] for i in range(len(A))]


if __name__ == "__main__":

    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    B = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    print(MatrixAdd(A, B))  # [[2, 2, 3], [4, 6, 6], [7, 8, 10]]
    print(MatrixMul(A, B))  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]