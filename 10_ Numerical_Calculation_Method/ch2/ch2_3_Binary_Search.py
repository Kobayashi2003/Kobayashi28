def binary_search(f, start, end, error):

    k = 0
    while True:
        mid = (start + end) / 2
        if f(mid) * f(start) < 0:
            end = mid
        elif f(mid) * f(end) < 0: 
            start = mid
        print("Iteration: ", k, " Root: ", mid, "value: ", f(mid))
        if 1 / 2**(k+1) < error or f(mid) == 0:
            print("Root is: ", mid)
            break
        k += 1

if __name__ == "__main__":
    f = lambda x : x**3 - x - 1
    start = 1
    end = 2
    error = 10**-3
    binary_search(f, start, end, error)