from math import sqrt

def primer_factors(n):
    factors = []
    for i in range(2, int(sqrt(n)) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return factors
