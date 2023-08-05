function [If,eps]=newtoncotes(f,a,b,n)   %牛顿-科特斯数值积分公式
    % n=1,即梯形公式
    % n=2，即辛普森公式
    % n=4，即科特斯公式

    h = (b-a)/n;
    xdata = a:h:b;

    C{1} = [1/2, 1/2];
    C{2} = [1/6, 4/6, 1/6];
    C{4} = [7/90, 32/90, 12/90, 32/90, 7/90];

    ydata = f(xdata);

    If = (b-a)*(C{n}*ydata');

    syms x;
    f = f(x);

    if n==1

        f2 = matlabFunction(diff(f,x,2));
        eps = max(abs(f2(xdata)))*(b-a)^3/12;
        
    elseif n==2

        f4 = matlabFunction(diff(f,x,4));
        eps = max(abs(f4(xdata)))*(b-a)^5/2880;

    elseif n==4

        f6 = matlabFunction(diff(f,x,6));
        eps = max(abs(f6(xdata)))*(b-a)^7/1935360;

    end

end