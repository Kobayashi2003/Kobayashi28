%%在这里disp对应的答案
x=input(''); %输入问题
%% 输入为x
%% 在下方写选择语句或分支语句

if -3 <= x && x < 5
    y = x^2 + 1;
elseif 5 <= x && x < 10
    y = abs(x-6);
elseif 10 <= x
    y = 1 / (x+1);
else
    y = 'error';
end


%% y为输出
disp(y)