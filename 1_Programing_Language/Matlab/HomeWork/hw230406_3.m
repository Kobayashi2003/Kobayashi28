[x, y, z] = meshgrid(-1.5:0.1:1.5);

% (x^2 + 9/4*y^2 + z^2 - 1)^3 - x^2*z^3 - 9/80*y^2*z^3 = 0
% use isosurface function

isosurface(x, y, z, (x.^2 + 9/4*y.^2 + z.^2 - 1).^3 - x.^2.*z.^3 - 9/80*y.^2.*z.^3, 0);