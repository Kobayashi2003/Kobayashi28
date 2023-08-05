A = [3 -0.1 -0.2; 
     0.1 7 -0.3; 
     0.3 -0.2 10];

b = [7.85; 
     -19.3; 
     71.4];

result = GaussPivot(A, b);
fprintf('x = \n');
disp(result);

[L, U] = my_LU(A);
fprintf('L = \n');
disp(L);
fprintf('U = \n');
disp(U);