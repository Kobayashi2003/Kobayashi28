clear; clc; close all;

filename = [pwd, '/demo.unknown'];

fileid = fopen(filename, 'r');

data_char = fscanf(fileid, '%c');
frewind(fileid);

data_u8 = fread(fileid, 'uint8');
frewind(fileid);

data_i16 = fread(fileid, 'int16');
frewind(fileid);

data_f32 = fread(fileid, 'float32');
fclose(fileid);
disp(data_char);
disp(data_u8);
disp(data_i16);
disp(data_f32);