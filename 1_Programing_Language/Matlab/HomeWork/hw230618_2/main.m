%测试代码
[a1,~,c]=CTn(@(x)sin(x)/x,0,1,5e-6,8);%已知n
disp(sprintf('%0.4f ',a1))
disp(sprintf('%0.5f ',c))
[a2,b,~]=CTn(@(x)sin(x)/x,0,1,5e-6);%未知n
disp(sprintf('%0.4f ',a2))
disp(sprintf('%0.0f ',b))