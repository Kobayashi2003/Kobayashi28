clear; clc; close all;

% Inverse function method generates random sequence and probability density function
n = 1:1000;
R = rand(1,1000);
inverse_function = @(x) sqrt(4*x);
X = inverse_function(R);

% mean and variance of the random sequence
m_X = mean(X);
v_X = var(X);

figure();

% plot the curve of the sequence
subplot(3, 1, 1);
plot(n,X);
title('Random sequence');
xlabel('n');
ylabel('X(n)');
grid on;

% plot the histogram of the sequence
subplot(3, 1, 2);
histogram(X, 100);
title('Histogram of the random sequence');
xlabel('X(n)');
ylabel('Frequency');
grid on;

% plot the probability density function
subplot(3, 1, 3);
[elements, centers] = hist(X, 100);
plot(centers, elements/sum(elements));
title('Probability density function');
xlabel('X(n)');
ylabel('f_X(x)');
grid on;