clear; clc; close all;

x = -16:0.5:16;
y = -10:0.5:10;

% x^3 + y^3 - 4xy + 1/6  x in [-4, 4], y in [-5, 5] 
% use ezplot to plot the function
subplot(3, 1, 1);
ezplot('x^3 + y^3 - 4*x*y + 1/6', [-4, 4, -5, 5]);


% sin((x^2 + y^2)^(1/2))  
% x in [-16, 16], y in [-10, 10]
%  meshgrid  mesh

subplot(3, 1, 2);
[X, Y] = meshgrid(x, y);
Z = sin((X.^2 + Y.^2).^(1/2));
mesh(X, Y, Z);


% base on (2), set color matrix C = x + y, use mesh function to plot the function again
% and use colorbar to show the color and value
subplot(3, 1, 3);
C = X + Y;
mesh(X, Y, Z, C);
colorbar;
