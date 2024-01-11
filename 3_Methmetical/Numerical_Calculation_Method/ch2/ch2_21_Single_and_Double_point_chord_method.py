def single_point_chord_method(f, x0, x1, n):
    x = x1
    for i in range(n):
        print(f"n: {i+1}, x: {x}, |xk - x0|: {abs(x-x0)}, f(x): {f(x)}")
        if f(x) == f(x0):
            break
        x = x- f(x)*(x-x0)/(f(x)-f(x0))
    return x

def double_point_chord_method(f, x0, x1, n):
    xk_prev = x0
    xk = x1
    for i in range(n):
        print(f"n: {i+1}, xk: {xk}, |xk - xk_prev|: {abs(xk-xk_prev)}, f(xk): {f(xk)}")
        if f(xk) == f(xk_prev):
            break
        xk_prev, xk = xk, xk - f(xk)*(xk-xk_prev)/(f(xk)-f(xk_prev))
    return xk

if __name__ == "__main__":
    f = lambda x: x**3 + 2*x**2 + 10*x - 20
    x0 = 1.5
    x1 = 1.4
    n = 10
    single_point_chord_method(f, x0, x1, n)
    print("=====================================")
    double_point_chord_method(f, x0, x1, n)
