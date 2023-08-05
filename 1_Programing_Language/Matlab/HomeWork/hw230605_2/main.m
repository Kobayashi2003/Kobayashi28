X = [0 1 4 5];
Y = [0 -2 -8 -4] ;
dx0 = 5/2; dxn = 19/4;
S = csfit(X,Y,dx0,dxn);
disp(S)