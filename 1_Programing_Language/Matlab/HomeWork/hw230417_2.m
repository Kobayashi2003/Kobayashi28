clear; clc; close all;

ilename = [pwd, '/class1.txt'];

% find the student who has the highest Chinese score

% Name,Chinese,Math,English,Physics,Chemistry,Biology

fileid = fopen(filename, 'r' );

data_char = textscan(fileid, '%s %s %s %s %s %s %s', 'Delimiter' , ',');

fclose(fileid);

name = data_char{1};
Chinese_score = str2double(data_char{2});

[~,index] = max(Chinese_score);
disp(name{index});