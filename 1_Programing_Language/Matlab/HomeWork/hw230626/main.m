f = @(x)(x^10 - 1);
df = @(x)(10*x^9);
x0 = 0.5;
es = 10^-6;
n = 100;

disp(newtraph(f,df,x0,es,n));