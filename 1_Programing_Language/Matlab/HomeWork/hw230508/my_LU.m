function [L,U] = my_LU(m)
    % my_LU(m) decomposes a matrix m into a lower triangular matrix L and an upper triangular matrix U
    % 
    % Inputs:
    % m - a square matrix
    % 
    % Outputs:
    % L - a lower triangular matrix
    % U - an upper triangular matrix
    % 

    % check if m is a square matrix
    [r, c] = size(m);
    if r ~= c
        error('m must be a square matrix');
    end

    % initialize L and U
    L = eye(r);
    U = zeros(r,c);

    for j = 1:c
        for i = 1:r
            if i <= j
                U(i,j) = m(i,j) - L(i,1:i-1)*U(1:i-1,j);
            else
                L(i,j) = (m(i,j) - L(i,1:i-1)*U(1:i-1,j))/U(j,j);
            end
        end
    end
end