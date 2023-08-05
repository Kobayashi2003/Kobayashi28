% 补充cholesky_decomposition函数，将A矩阵分解为下三角矩阵L和上三角矩阵U
function [L, U] = cholesky_decomposition(A)
    n = size(A, 1);
    L = zeros(n);
    for j = 1:n
        L(j, j) = sqrt(A(j, j) - L(j, 1:j-1) * L(j, 1:j-1)');
        for i = j+1:n
            L(i, j) = (A(i, j) - L(i, 1:j-1) * L(j, 1:j-1)') / L(j, j);
        end
    end
    U = L';
end