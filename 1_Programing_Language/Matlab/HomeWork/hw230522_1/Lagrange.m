function yint = Lagrange(x, y, xx)
    
    yint = 0;
    for k = 1:length(y)
        w = 1;
        for i = 1:length(x)
            if (i ~= k)
                w = w * (xx - x(i)) / (x(k) - x(i));
            end
        end
        yint = yint + w * y(k);
    end

end