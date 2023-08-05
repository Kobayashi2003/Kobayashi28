function output = fun1(input)
    max_num = max(input);
    min_num = min(input);
    mean_num = mean(input);
    var_num = var(input);
    output = [max_num, min_num, mean_num, var_num];
end