import math

# Iterative method
def iterative(f, L, x0, error):
    count_error = lambda xk, xk_prev: L/(1-L)*abs(xk-xk_prev)
    xk = f(x0)
    xk_prev = x0
    k = 1
    while True:
        print(f"k: {k}, xk: {xk}, |xk - xk_prev|: {abs(xk - xk_prev)}, error: {count_error(xk, xk_prev)}")
        if count_error(xk, xk_prev) < error:
            break
        k += 1
        xk_prev = xk
        xk = f(xk)
    return xk

if __name__ == "__main__":
    f = lambda x: 4 + 2 / 3 *math.cos(x)
    L = 2 / 3
    x0 = 4
    error = 10**-3
    print(iterative(f, L, x0, error))