% x=[10 20 30 40 50 60 70 80];
% y=[25 70 380 550 610 1220 830 1450];
% y = a(2) + a(1)*x

x = [0, 0.2, 0.4, 0.6, 0.8];
y = [0.9, 1.9, 2.8, 3.3, 4.2];


a = linregr(x,y);
disp(sprintf('%0.4f ',a))