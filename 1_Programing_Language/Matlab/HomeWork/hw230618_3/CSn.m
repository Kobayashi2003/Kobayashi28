function [Sn2,n1,eps] =CSn(f,a,b,eps,n)
    %复合辛普森求积公式
    %f为函数；a、b 为积分上下界 eps为误差； 输入n，n1：分段数(如n1=8意思为分为8等份),复合辛普森公式n1=2n
    %当n已知时，主要输出Sn2（积分值）和eps（估计误差）
    %当n未知时，主要输出Sn2和n,Sn2、eps、n为double
    %本题中求导数最大值时，其四阶导数F''''(m)中建议m=a:(b-a)/1000:b，间隔不宜过小
    format long
    if nargin<3
        error('at least 3 input arguments required');
    end
    if ~b>a
        error('upper bound must be greater than lower');
    end
    % 勿动，否则由于精度问题，会出现零除报错
    a=a+1e-50;
    b=b+1e-50;
    %%%% your code
    syms x;
    y = f(x);
    d4y = matlabFunction(diff(y,4));

    if nargin<5 || isempty(n)
        %未知n
        n1 = 0;
        eps_tmp = 1 + eps;
        while eps_tmp > eps
            n1 = n1 + 2;
            h = (b-a) / n1 * 2;
            eps_tmp = (b-a)*h^4/2880*max(abs(d4y(a:(b-a)/1000:b)));
        end

        xdata = a:h:b;
        Sn2 = 0;
        for i = 1:n1/2
            Sn2 = Sn2 + h/6 * (f(xdata(i)) + 4*f((xdata(i) + xdata(i+1)) / 2) + f(xdata(i+1)));
        end

        eps = eps_tmp;

    else
        %已知n
        n1 = 2 * n;
        h = (b-a) / n1 * 2;

        xdata = a:h:b;
        Sn2 = 0;
        for i = 1:n1/2
            Sn2 = Sn2 + h/6 * (f(xdata(i)) + 4*f((xdata(i) + xdata(i+1)) / 2) + f(xdata(i+1)));
        end
    
        eps = (b-a)*h^4/2880*max(abs(d4y(a:(b-a)/1000:b)));

    end
end