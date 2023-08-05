clear; clc; close all;

filename = [pwd, '/class1.txt'];
outfile = 'class1_total.txt';

% Read the data in the file
fileid = fopen(filename);
data_char = textscan(fileid, '%s %s %s %s %s %s %s', 'Delimiter' , ',');
fclose(fileid);

% Name,Chinese,Math,English,Physics,Chemistry,Biology
Name = data_char{1};
Chinese_score = str2double(data_char{2});
Math_score = str2double(data_char{3});
English_score = str2double(data_char{4});
Physics_score = str2double(data_char{5});
Chemistry_score = str2double(data_char{6});
Biology_score = str2double(data_char{7});

% Calculate the total score
total_score = Chinese_score + Math_score + English_score + Physics_score + Chemistry_score + Biology_score;

% Add a new column to the data
data_char{8} = num2cell(total_score);

% Write the data to a new file
fileid = fopen(outfile, 'w' );
fprintf(fileid, '%s\n', 'Name,Chinese,Math,English,Physics,Chemistry,Biology,Total');

for i = 2 :length(Name)
    fprintf(fileid, '%s,%d,%d,%d,%d,%d,%d,%d\n' , Name{i}, Chinese_score(i), Math_score(i), English_score(i), Physics_score(i), Chemistry_score(i), Biology_score(i), total_score(i));
end

fclose(fileid);