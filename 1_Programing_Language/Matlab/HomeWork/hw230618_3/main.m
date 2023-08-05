% 测试代码
[a1,~,c]=CSn(@(x)sin(x)/x,0,1,5e-6,4);%已知n
disp(sprintf('%0.3f ',a1));
disp(sprintf('%0.8f ',c));
[a2,b,~]=CSn(@(x)sin(x)/x,0,1,5e-6);%未知n
disp(sprintf('%0.3f ',a2));
disp(sprintf('%0.0f ',b));
