clear; clc; close all;

x = linspace(-10,10,1000);

y = cos(x) + sin(2*x);
plot(x,y,'r--','LineWidth',2);

hold on;

y = cos(x).^2;
plot(x,y,'g-','LineWidth',2);

xlabel('x');
ylabel('y');

legend('cos(x) + sin(2x)','cos^2(x)');

grid on;

hold off;