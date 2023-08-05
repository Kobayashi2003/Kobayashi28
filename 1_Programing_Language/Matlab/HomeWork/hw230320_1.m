% warning('off','all');
% graphics_toolkit('gnuplot')


x=0:0.001:20;
f=0.5*exp(-0.3*x);
figure(1);
 
subplot(1,2,1);

plot(x, f);
xlabel('x');
ylabel('y');
title('figure 1');
legend('f(x) = 0.5e^{-0.3x}');
grid on;

subplot(1,2,2);

semilogy(x, f);
xlabel('x');
ylabel('ln(y)');
title('figure 2');
legend('f(x) = 0.5e^{-0.3x}');
grid on;



% sa=pwd;
% print(1,'-djpeg','./plotting/answer/picture1.jpg');
% run('./plotting/generate.m');
% system('python3  ./plotting/compareImg.py');