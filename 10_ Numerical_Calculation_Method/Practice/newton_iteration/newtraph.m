function result = newtraph(f, df, x0, tol, maxiter)
    % Newton's method for finding a root of f(x) = 0
    %
    % Input:
    % f - function handle for f(x)
    % df - function handle for f'(x)
    % x0 - initial guess
    % tol - tolerance
    % maxiter - maximum number of iterations
    %
    % Output:
    % result - root of f(x) = 0
    %
    if df(x0) == 0
        error('Derivative is zero at initial guess');
    end

    xn = x0; xn_pre = x0; k = 0;
    while k < maxiter
        xn = xn - f(xn)/df(xn);
        fprintf('k = %d, x = %f\n', k, xn);
        if abs(xn - xn_pre) < tol
            result = xn;
            return;
        end
        xn_pre = xn;
        k = k + 1;
    end
end