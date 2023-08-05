sum = 0;

for i = 1:1:30
    sum = sum + 2^(i-1);
end
% 不使用科学计数法输出

format long g

disp(sum)
