% 设计一个用于计算个人所得税的程序，假设个人所得税的缴纳标准为：  

%     月收入少于等于800元者不缴税
%     超过800元部分，缴税5%
%     超出2000元部分，缴税10%
%     超出5000元部分，缴税20%
%     超出10000元部分，缴税30%
%     超出100000元部分，缴税40%

% 提示：如果输入工资有误，则tax为‘error’

salary=input('');

tax=0;
%% YOUR CODE HERE
if salary < 0
    tax='error';
elseif salary<=800
    tax=0;
elseif salary<=2000
    tax=0.05*(salary-800);
elseif salary <= 5000
    tax=0.05*1200+0.1*(salary-2000);
elseif salary <= 10000
    tax=0.05*1200+0.1*3000+0.2*(salary-5000);
elseif salary <= 100000
    tax=0.05*1200+0.1*3000+0.2*5000+0.3*(salary-10000);
elseif salary > 100000
    tax=0.05*1200+0.1*3000+0.2*5000+0.3*90000+0.4*(salary-100000);
end

%% Output
disp(tax)