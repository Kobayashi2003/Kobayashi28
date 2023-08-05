load("bicycle.mat")

% use hist function
% x: the grayscale values
% y: the number of pixels with the corresponding grayscale value

% usable value: image [ type: uint8 size: 822, 1237 ]

% reshape the image into a vector

% image = double(image(:)./(max(image(:))));
image = im2double(image);

% hist(image);
histogram(image(:), 10);