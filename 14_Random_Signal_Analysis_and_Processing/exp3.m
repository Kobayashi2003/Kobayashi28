clc; clear; close all;

%% generate X(n) by impulse response method 

% generate h(n) by freqz and ifft
% - B: numerator
% - A: denominator
B = 1;
A = [1 0.8];
[H, w] = freqz(B, A, (0:2*pi/1000:2*pi).');
h = ifft(H);

% generate W(n) by randn
Sigma = 2; Ts = 1; Fs = 1/Ts;
W = Sigma .* randn(500, 1) + 0;

% X(n) = W(n) * h(n)
X = conv(W,h);
X = X(1:500);
figure, plot(abs(X)); xlabel('order'); ylabel('amplitude'); 

% calculate mean and variance
mX = mean(X); vX = var(X);


% theorectical Rx and Gx
Gx = abs(H) .^ 2 * 4;
fset = (0:length(Gx)-1) * Fs/length(Gx);
figure, plot(fset, Gx); xlabel('frequency'); ylabel('amplitude(dB)');
Rx = fftshift(ifft(Gx));
figure, plot(abs(Rx)); xlabel('order'); ylabel('amplitude'); axis([0 1000 0 12]);


% estimated Rx and Gx
Rx1 = xcorr(X);
figure, plot(abs(Rx1)); xlabel('order'); ylabel('amplitude');
nfft = 1024;
window = hann(length(X));
[Pxx, fset2] = periodogram(X, window, nfft, Fs);
figure, plot(fset2, Pxx); xlabel('frequency'); ylabel('amplitude(dB)');