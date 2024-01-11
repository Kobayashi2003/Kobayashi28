import numpy as np

# Jacobain iteration method
def Jacobi(A, b, X, n):
    if np.linalg.det(A) == 0:
        print('A is singular matrix')
        return
    D = np.diag(np.diag(A))
    if np.linalg.det(D) == 0:
        print('D is singular matrix')
        return 
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    J = np.linalg.inv(D)@(L+U)
    if is_convergent(J) == False:
        print('J is not convergent')
        return
    f = np.linalg.inv(D)@b
    for i in range(n):
        X_old = X
        X = J@X + f
        print(f"X{i+1} = {X} \t\tmax(abs(X-X_old)) = {max(abs(X-X_old))}")
        if (max(abs(X-X_old)) < 1e-9):
            break


# Gauss-Seidel iteration method
def Gauss_Seidel(A, b, X, n):
    if np.linalg.det(A) == 0:
        print('A is singular matrix')
        return
    D = np.diag(np.diag(A))
    if np.linalg.det(D) == 0:
        print('D is singular matrix')
        return
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    G = np.linalg.inv(D-L)@U
    if is_convergent(G) == False:
        print('G is not convergent')
        return
    f = np.linalg.inv(D-L)@b
    for i in range(n):
        X_old = X
        X = G@X + f
        print(f"X{i+1} = {X} \t\tmax(abs(X-X_old)) = {max(abs(X-X_old))}")
        if (max(abs(X-X_old)) < 1e-9):
            break


# Successive over-relaxation method
def SOR(A, b, X, n, w):
    if np.linalg.det(A) == 0:
        print('A is singular matrix')
        return
    D = np.diag(np.diag(A))
    if np.linalg.det(D) == 0:
        print('D is singular matrix')
        return
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    S = np.linalg.inv(D-w*L)@((1-w)*D+w*U)
    if is_convergent(S) == False:
        print('S is not convergent')
        return
    f = np.linalg.inv(D-w*L)@w*b
    for i in range(n):
        X = S@X + f
        print('X%d = '%(i+1), X)


# judge if the iteration method is convergent
def is_convergent(fai):
    # characteristic value
    lambda_values = np.linalg.eigvals(fai)
    # spectral radius
    r = np.max(np.abs(lambda_values))
    if r < 1:
        if (abs(r-1) < 1e-9):
            return False
        else:
            return True
    else:
        return False


def main():
    # AX = b
    A = np.array([[10, -2, -2],
                  [-2, 10, -1],
                  [-1, -2, 3]])
    b = np.array([1, 0.5, 1])
    X = np.array([0, 0, 0])

    print('Jacobi iteration method')
    n = 20
    Jacobi(A, b, X, n)

    print()

    print('Gauss-Seidel iteration method')
    n = 15
    Gauss_Seidel(A, b, X, n)

if __name__ == '__main__':
    main()