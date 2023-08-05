% 补充GaussSeide函数，其中A为系数矩阵, b为常数向量, max_iter为最大迭代次数, tol为收敛条件
function x = GaussSeidel(A, b, max_iter, tol)
    D = diag(diag(A));
    L = -tril(A, -1);
    U = -triu(A, 1);
    G = (D - L) \ U;
    f = (D - L) \ b;
    x = zeros(size(b));
    for k = 1:max_iter
        x = G * x + f;
        if norm(x - G * x - f) < tol
            break;
        end
    end
end