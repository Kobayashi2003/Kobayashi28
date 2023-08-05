% spalloc
% create a 5x5 sparse matrix with 10 non-zero elements
S = spalloc(5,5,10);
% the left upper corner of the matrix is filled with a 2x2 magic square
S(1:2,1:2) = magic(2);
disp(S);