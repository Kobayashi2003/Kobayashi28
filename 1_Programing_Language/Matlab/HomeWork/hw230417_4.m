clear; clc; close all;

filename1 = [pwd, '/class1.txt'];
filename2 = [pwd, '/class2.txt'];
outfile = 'report.txt';

% Read the data in the file
fileid1 = fopen(filename1);
fileid2 = fopen(filename2);

% Read the data in the file
data_char1 = textscan(fileid1, '%s %s %s %s %s %s %s', 'Delimiter' , ',');
data_char2 = textscan(fileid2, '%s %s %s %s %s %s %s', 'Delimiter' , ',');

% Close the file
fclose(fileid1);
fclose(fileid2);

% Name,Chinese,Math,English,Physics,Chemistry,Biology

% delete the first row in the data_char2
for i = 1:size(data_char2, 2)
    data_char2{i}(1) = [];
end

% connect two cell
data_char = cell(1, size(data_char1, 2));
for i = 1:size(data_char2, 2)
    data_char{i} = [data_char1{i}; data_char2{i}];
end

% calculate the total score

Name = data_char{1};
Chinese_score = str2double(data_char{2});
Math_score = str2double(data_char{3});
English_score = str2double(data_char{4});
Physics_score = str2double(data_char{5});
Chemistry_score = str2double(data_char{6});
Biology_score = str2double(data_char{7});

total_score = Chinese_score + Math_score + English_score + Physics_score + Chemistry_score + Biology_score;

% sort all the data by total score
[total_score, index] = sort(total_score, 'descend' );
Name = Name(index);
Chinese_score = Chinese_score(index);
Math_score = Math_score(index);
English_score = English_score(index);
Physics_score = Physics_score(index);
Chemistry_score = Chemistry_score(index);
Biology_score = Biology_score(index);

% output the data in the file
fileid = fopen(outfile, 'w' );
fprintf(fileid, '%s\n', 'Name,Chinese,Math,English,Physics,Chemistry,Biology,Total' );
for i = 2:size(Name, 1)
    fprintf(fileid, '%s,%d,%d,%d,%d,%d,%d,%d\n' , Name{i}, Chinese_score(i), Math_score(i), English_score(i), Physics_score(i), Chemistry_score(i), Biology_score(i), total_score(i));
end
fclose(fileid);