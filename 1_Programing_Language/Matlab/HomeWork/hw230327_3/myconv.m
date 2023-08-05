function result = myconv(vet1, vet2)
    if (size(vet1,1) ~= 1 || size(vet2,1) ~= 1) || isnumeric(vet1) == 0 || isnumeric(vet2) == 0
        result = "Invalid Inputs";
        return
    end 
    result = zeros(1, length(vet1) + length(vet2) - 1);
    for i = 1:length(vet1)
        for j = 1:length(vet2)
            result(i + j - 1) = result(i + j - 1) + vet1(i) * vet2(j);
        end
    end
end