import math

# larange interpolation
def lagrange(x: float, xi: list, yi: list) -> float:
    """
    Lagrange interpolation
    :param x: x value
    :param xi: known x values
    :param yi: known y values
    :return: y(x)
    """
    n = len(xi)
    y = 0
    for k in range(n):
        p = 1
        for j in range(n):
            if j != k:
                p *= (x - xi[j]) / (xi[k] - xi[j])
        y += p * yi[k]
    return y

def truncation_error(x: float, xi: list, yi: list) -> float:
    """
    Truncation error
    :param x: x value
    :param xi: known x values
    :param yi: known y values
    :return: error
    """
    n = len(xi)
    p = 1
    for k in range(n):
        p *= (x - xi[k])
    return abs(max(yi) * p) / math.factorial(n)

def main():
    xi = [math.pi / 6, math.pi / 4, math.pi / 3]
    yi = [1/2, (2)**(1/2)/2, (3)**(1/2)/2]
    x = math.pi * 5 / 18
    print(lagrange(x, xi, yi))
    print(truncation_error(x, xi, yi))

if __name__ == '__main__':
    main()