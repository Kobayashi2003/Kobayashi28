function output = fun2(input)
    A = input(:,1:size(input,1));
    Y = input(:,end);
    if rank(A) < rank(input)
        output = 'No solution';
    elseif rank(A) == rank(input)
        if rank(A) == size(input, 1)
            X = A\Y;
            output = X;
        elseif rank(A) < size(input, 1)
            output = 'Infinite solutions';
        end
    end
end
