x = linspace(0,1,1000);
y = sin(2*pi*x);

% Plot the function
figure(1)
xlabel('x')
ylabel('y')
title('sin(2\pi x)')
plot(x,y,'k-')
print -dpng 'sin.png'