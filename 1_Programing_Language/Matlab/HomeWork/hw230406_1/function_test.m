function y = function_test(str1, str2)
    
    if strcmp(str1, str2)
        y = upper(str1);
    else
        y = [str1, str2];
        a_place = strfind(y, 'a');
        if ~isempty(a_place)
            y = num2str(a_place);
        else
            y = num2str(-1);
        end
    end
end
