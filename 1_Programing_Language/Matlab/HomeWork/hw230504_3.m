clear; clc; close all;

[X, Y] = meshgrid(-10:1:10);
Z = sin((X.^2+Y.^2).^(1/2)) ./ (X.^2+Y.^2).^(1/2);

% f(X,Y) = sin((x^2+y^2)^(1/2)) / (x^2+y^2)^(1/2)

figure();
subplot(1, 2, 1);
% mesh
mesh(X, Y, Z);

subplot(1, 2, 2);
surf(X, Y, Z);