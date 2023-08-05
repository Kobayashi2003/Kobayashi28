function S = csfit(X,Y,dx0,dxn)
% Input X is the 1xn abscissa vector
%       Y is the 1xn ordinate vector
%       dxo=S'(x0) first derivative boundary condition
%       dxn=S'(xn) first derivative boundary condition 
% Output S: rows of S are the coefficients, in descending order, for the cubic interpolants

%%%%%%%%%%%%%%% YOUR CODE HERE %%%%%%%%%%%%%%%

    N = length(X);
    H = diff(X); A = diff(Y); B = A./H; C = diff(B);
    D = zeros(1,N); U = zeros(N-2,1); L = zeros(N-2,1);
    for k=2:N-1
        D(k) = 6*C(k-1)/(H(k-1)+H(k));
    end
    D(1) = 6*(B(1)-dx0)/H(1);
    D(N) = 6*(dxn-B(N-1))/H(N-1);
    for k=1:N-2
        U(k) = H(k)/(H(k)+H(k+1));
        L(k) = 1-U(k);
    end
    Q=2*eye(N); Q(1,2)=1; Q(N,N-1)=1;
    for k=1:N-2
        Q(k+1,k+2) = L(k);
        Q(k+1,k) = U(k);
    end

    M=Q\D';
    S = zeros(N-1,4);
    for k=1:N-1
        S(k,1)=(M(k+1)-M(k))/(6*H(k));
        S(k,2)=(M(k)*X(k+1)-M(k+1)*X(k))/(2*H(k));
        S(k,3)=(M(k+1)*(X(k)^2)-M(k)*(X(k+1)^2))/(2*H(k))+(Y(k+1)-Y(k))/H(k)+(M(k)-M(k+1))*H(k)/6;
        S(k,4)=(M(k)*(X(k+1)^3)-M(k+1)*(X(k)^3))/(6*H(k))+(Y(k)*X(k+1)-Y(k+1)*X(k))/H(k)+(X(k)*M(k+1)-X(k+1)*M(k))*H(k)/6;
    end

end