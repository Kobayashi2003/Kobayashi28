clear; clc; close all;

x = -2:0.2:2;

figure

% y = (2*(x^2)^(1/2)-x^2)^(1/2), x in [-2, 2] green . line
y = (2*(x.^2).^(1/2)-x.^2).^(1/2);
plot(x, y, 'g.-')
% z = arcsin(|x| - 1) - pi/2, x in [-2, 2]  blue -- line
z = asin(abs(x) - 1) - pi/2;
hold on
plot(x, z, 'b--')

xlabel('x');
ylabel('y');