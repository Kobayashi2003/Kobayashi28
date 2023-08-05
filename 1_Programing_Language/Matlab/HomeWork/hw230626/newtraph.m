function x = newtraph(f, df, x0, esp, n)
    x = x0;
    for i = 1:n
        x = x - f(x)/df(x);
        if abs(f(x)) < esp
            break
        end
    end
end
