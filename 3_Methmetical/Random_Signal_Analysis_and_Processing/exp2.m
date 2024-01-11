clc; clear; close all;

Sigma = 1; a = 0.8; M = 1000; m = 0:1:M;
Rx = Sigma^2 / (1 - a^2) * a.^abs(m);
mule = 0;

% calculate covariance matrix
N = 1000;
K = zeros(N, N);
for i = 1:N
    K(i, :) = cat(2, Rx(i:-1:1), Rx(2:N-i+1));
end

figure;

% generate normal distribution random sequence
subplot(3, 1, 1);

A = chol(K).';
u = randn(N, 1);
x = A * u + mule;

plot(x);
xlabel('n'); ylabel('x(n)'); title('x(n)');


% draw autocorrelation function of x
subplot(3, 1, 2);

Rx = cat(2, Rx(N:-1:2), Rx(1:N));
plot(-N+1:N-1, Rx, 'b');

hold on;

Rx = xcorr(x, 'biased');
plot(-N+1:N-1, Rx, 'r');

hold off;

xlabel('m'); ylabel('Rx(m)'); title('Rx(m)');
legend('theoretical', 'estimated');


% draw power spectral density of x (double-sided)
subplot(3, 1, 3);

Gx = fftshift(fft(Rx));
w = linspace(-pi, pi, 2*N-1);
plot(w, Gx);
xlabel('w'); ylabel('Gx(w)'); title('Gx(w)');