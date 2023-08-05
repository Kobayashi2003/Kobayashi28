% f(x) = x^10 - 1

f = @(x) x.^10 - 1;
df = @(x) 10*x.^9;
x0 = 0.5;
tol = 1e-10;
maxiter = 100;

% draw function f(x)
figure(1)
x = linspace(0.5, 1.5, 1000);
y = f(x);
plot(x, y, "b-");
hold on;
plot(x, zeros(size(x)), "r-");
hold off;
grid on;

% Newton's method
result = newtraph(f, df, x0, tol, maxiter);
fprintf('Newton''s method: %d\n', result);