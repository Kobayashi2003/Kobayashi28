# Aitken

import numpy as np

def aitken(x, y, x0):
    """
    Aitken interpolation
    :param x: x values
    :param y: y values
    :param x0: x value
    :return: y(x0)
    """
    n = len(x)
    y0 = np.zeros(n)
    for k in range(n):
        for i in range(n - k):
            if k == 0:
                y0[i] = y[i]
            else:
                y0[i] = (x0 - x[i]) / (x[i + k] - x[i]) * y0[i + 1] + \
                        (x[i + k] - x0) / (x[i + k] - x[i]) * y0[i]
    return y0[0]

def main():
    x = [0, 1, -1, 2, -2]
    y = [1, 3, 1/3, 9, 1//9]
    x0 = 0.5
    print(aitken(x, y, x0))

if __name__ == '__main__':
    main()