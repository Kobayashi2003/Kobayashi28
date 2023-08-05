%% initial
clc; clear; close all;
%% read image
img = imread("image.png");
figure, 
subplot(331), imshow(img); grid on; title("Original image");
title("image colorful image");

%% conver to gray
gray = rgb2gray(img);
r = img (:,:,1);
g = img (:,:,2);
b = img (:,:,3);
subplot(332), imshow(gray); grid on; title("gray");
subplot(333), imshow(r); grid on; title("r");
subplot(334), imshow(g); grid on; title("g");
subplot(335), imshow(b); grid on; title("b");

%% sub image
subsize = 1 * size(gray) / 2;
subsize = floor(subsize);
subplot(336), imshow(gray(1:subsize(1), 1:subsize(2))); grid on; title("sub");

%% zero specified pixels
gray_tmp = gray;
gray_tmp(1:2:end, 1:2:end) = 0;
gray_tmp(2:2:end, 2:2:end) = 0;
subplot(337), imshow(gray_tmp); grid on; title("zero specified pixels");

%% binarization
gate = 60;
ord = gray > gate;
gray(ord) = 60;
gray(~ord) = 0;
subplot(337), imshow(gray); grid on; title("binarization");
