% （1）四年一闰百年不闰：即如果year能够被4整除，但是不能被100整除，则year是闰年。
% （2）每四百年再一闰：如果year能够被400整除，则year是闰年。

% 小问1：找出距离3801年最近的闰年，并输出
% 小问2：找出1-3000中的所有闰年，按从小到大的顺序存于数组A，并输出。

%第一问
year1 = 3801;
target_year = 0;
%begin
i = 0;
while true
    if mod(year1+i,4) == 0 && mod(year1+i,100) ~= 0
        target_year = year1+i;
        break;
    elseif mod(year1+i,400) == 0
        target_year = year1+i;
        break;
    elseif mod(year1-i,4) == 0 && mod(year1-i,100) ~= 0
        target_year = year1-i;
        break;
    elseif mod(year1-i,400) == 0
        target_year = year1-i;
        break;
    end
    i = i+1;
end
%end
disp(target_year)

%第二问
A = [];
%begin
for year = 1:3000
    if mod(year,4) == 0 && mod(year,100) ~= 0
        A = [A,year];
    elseif mod(year,400) == 0
        A = [A,year];
    end
end
 
%end
    
disp(A(:))