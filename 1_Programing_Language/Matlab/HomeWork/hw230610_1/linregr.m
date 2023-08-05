function a = linregr(x,y)
    % input: x=independent variable 
    %        y= dependent variable 
    % output: a=vector of slope,a(1),and intercept, a(2)

    n = length(x);
    if length(y)~=n
        error('x and y must be same length');
    end
    % you code
    
    X = [sum(x.^2) sum(x); sum(x) n];
    Y = [sum(x.*y); sum(y)];
    a = X\Y;
   
end