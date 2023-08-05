feature = { "surfarea", "grayvol" };
roi = { "bankssts", "coneus", "fusiform", "inferior" };

% change into the form like"banksstssurfacea" 
roi_feature = cell(length(feature),length(roi));
for i = 1:length(feature)
    for j = 1:length(roi)
        roi_feature{i,j} = roi{j}+feature{i}; % [roi{j}, feature{i}]
    end
end

disp(roi_feature)