x=[-2 -1 0 1 2];
y=[-0.1 0.1 0.4 0.9 1.6];
%y = p(1) + p(2)*x + p(3)*x.^2 + p(4)*x.^3
p1=Polynomial(x,y,2);
p2=Polynomial(x,y,3);
disp(sprintf('%0.3f ',p1))
disp(sprintf('%0.3f ',p2))