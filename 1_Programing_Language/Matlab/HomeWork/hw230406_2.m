% t blong to [-0.5, 0.5]
% s(t) = exp(j*pi*K*t^2), K = 100
% draw the real part and the imaginary part of s(t)
clear; clc; close all;

t = linspace(-0.5, 0.5, 1000);
K = 100;
s = exp(1i*pi*K*t.^2);

figure
subplot(2,1,1)
plot(t,real(s));
title('Real');
ylabel('Amplitude');
xlabel('t');

subplot(2,1,2)
plot(t,imag(s));
title('Image');
ylabel('Amplitude');
xlabel('t');