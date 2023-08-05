function result = GaussPivot(A, b)
    %GaussPivot - Description
    % 
    % Inputs:
    %   A - coefficient matrix
    %   b - right hand side vector
    %
    % Outputs:
    %  result - solution vector
    % 

    n = length(b);
    for k = 1:n-1
        % partial pivoting
        [~, i] = max(abs(A(k:n, k)));
        i = i + k - 1;
        if i ~= k
            A([k, i], :) = A([i, k], :);
            b([k, i]) = b([i, k]);
        end

        % elimination
        for i = k+1:n
            m = A(i, k) / A(k, k);
            A(i, :) = A(i, :) - m * A(k, :);
            b(i) = b(i) - m * b(k);
        end
    end

    % back substitution
    result = zeros(n, 1);
    result(n) = b(n) / A(n, n);
    for i = n-1:-1:1
        result(i) = (b(i) - A(i, i+1:n) * result(i+1:n)) / A(i, i);
    end
end