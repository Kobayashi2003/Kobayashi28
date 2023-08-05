function [Tn,n,eps]=CTn(f,a,b,eps,n)
    %f为函数；a、b 为积分上下界 eps为误差； n1：分段数(如n1=8意思为分为8等份)
    %当n已知时，主要输出Tn（积分值）和eps（估计误差）
    %当n未知时，主要输出Tn和n1
    %Tn为积分值，Tn、eps、n为double
    %复合梯形公式

    % 0.9457 
    % 0.00043 
    % 0.9461
    % 75

    format long
    if nargin<3
        error('at least 3 input arguments required');
    end
    if ~b>a
        error('upper bound must be greater than lower');
    end
    % 勿动，否则由于精度问题，会出现零除报错
    a=a+1e-100;
    b=b+1e-100;
    %your code

    syms x;
    y = f(x);
    d2y = matlabFunction(diff(y, x, 2));


    if nargin<5 || isempty(n)
        %未知n
        n = 0;
        eps_tmp = eps + 1;
        while eps_tmp > eps

            n = n + 1;
            h = (b-a) / n;
            xdata = a:h:b;
            ydata = zeros(1, length(xdata));
            for i = 1:length(xdata)
                ydata(i) = f(xdata(i));
            end

            eps_tmp = (b-a) * h^2 / 12 * max(abs(d2y(xdata)));
        end

        Tn = h * (sum(ydata) - (ydata(1) + ydata(end)) / 2);
        eps = eps_tmp;

    else
    %已知n
        h = (b-a) / n;
        xdata = a:h:b;
        ydata = zeros(1, length(xdata));
        for i = 1:length(xdata)
            ydata(i) = f(xdata(i));
        end

        Tn = h * (sum(ydata) - (ydata(1) + ydata(end)) / 2);
        eps = (b - a) * h^2 / 12 * max(abs(d2y(xdata)));

    end

end
