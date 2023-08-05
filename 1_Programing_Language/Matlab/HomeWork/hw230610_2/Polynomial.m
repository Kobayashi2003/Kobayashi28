function P=Polynomial(x,y,m)  
    % input: x,y为序列长度相等的数据向量
    %        m = 拟合多项式次数
    % output:P = 拟合多项式系数

    X = zeros(m+1,m+1);
    Y = zeros(m+1,1);

    for i = 1:m+1
        for j = 1:m+1
            X(i,j) = sum(x.^(i+j-2));
        end
        Y(i) = sum(x.^(i-1).*y);
    end

    P = X\Y;

end

