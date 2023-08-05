% mchol函数为求解方程组的函数
function [L, y, x] = mchol(A, b)
    % Cholesky 分解
    [L, U] = cholesky_decomposition(A);
    
    % 前向替换求解 y
    y = forward_substitution(L, b);
    
    % 后向替换求解 x
    x = back_substitution(U, y);
end