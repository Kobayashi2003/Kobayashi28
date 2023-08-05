function x = my_SOR(A, b)

    x = zeros(size(b));
    D = diag(diag(A));
    L = -tril(A, -1);
    U = -triu(A, 1);
    w = 0.8;
    S = (D - L.*w) \ (D.*(1-w) + U.*w);
    f = (D - L.*w) \ (b.*w);
    for i = 1:50
        x = S * x + f;
    end

end