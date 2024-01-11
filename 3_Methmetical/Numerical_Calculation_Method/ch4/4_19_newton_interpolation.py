# newton interpolation

def newton_interpolation(x: float, xi: list, yi: list) -> float:
    """
    Newton interpolation
    :param x: x value
    :param xi: known x values
    :param yi: known y values
    :return: y(x)
    """
    n = len(xi)
    y = 0
    for k in range(n):
        p = 1
        for j in range(k):
            p *= (x - xi[j])
        y += p * divided_difference(xi, yi, k)
    return y

def divided_difference(xi: list, yi: list, k: int) -> float:
    """
    Divided difference
    :param xi: known x values
    :param yi: known y values
    :param k: number of known values
    :return: divided difference
    """
    if k == 0:
        return yi[0]
    else:
        return (divided_difference(xi, yi, k - 1) - divided_difference(xi[1:], yi[1:], k - 1)) / (xi[0] - xi[k])


def main():
    xi = [0, 1, -1, 2, -2]
    yi = [1, 3, 1/3, 9, 1//9]
    x = 0.5
    print(newton_interpolation(x, xi, yi))

if __name__ == '__main__':
    main()