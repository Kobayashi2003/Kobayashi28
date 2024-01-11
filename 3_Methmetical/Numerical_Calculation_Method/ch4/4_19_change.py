# newton interpolation

def newton_interpolation(x: float, xi: list, yi: list, N: int = 0) -> float:

    if N == 0:
        N = len(xi)
    n = len(xi)
    y = 0

    for i in range(n-1):
        print("Iteration: ", i+1)
        for j in range(n-1-i):
            yi[j] = (yi[j+1] - yi[j]) / (xi[i+j+1] - xi[j])
            print(yi[j], end=' ')
        print()
        p = 1
        for k in range(i+1):
            p *= (x - xi[k])
        y += p * yi[0]
        if i == N-1:
            break
    return y

def main():
    xi = [0, 0.2, 0.3, 0.5]
    yi = [0, 0.20134, 0.30452, 0.52110]
    x = 0.23
    result = newton_interpolation(x, xi, yi, 2)
    print(f"y({x}) = {result}")

    print()

    xi = [0, 0.2, 0.3, 0.5]
    yi = [0, 0.20134, 0.30452, 0.52110]
    x = 0.23
    print(f"y({x}) = {newton_interpolation(x, xi, yi, 3)}")

if __name__ == '__main__':
    main()
