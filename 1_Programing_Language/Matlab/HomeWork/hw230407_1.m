% sparse matrix

m = eye(10, 10) .* 2.^(1:1:10);
disp(sparse(m));