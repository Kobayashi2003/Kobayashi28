import numba
import numpy
import time

@numba.jit  
def test():
    a = numpy.random.rand(10000, 10000)
    b = numpy.random.rand(10000, 10000)
    c = numpy.zeros((10000, 10000))
    for i in range(10000):
        for j in range(10000):
            c[i, j] = a[i, j] + b[i, j]

def test2():
    a = numpy.random.rand(10000, 10000)
    b = numpy.random.rand(10000, 10000)
    c = numpy.zeros((10000, 10000))
    for i in range(10000):
        for j in range(10000):
            c[i, j] = a[i, j] + b[i, j]

start = time.time()
test()
print("Time with numba.jit: ", time.time()-start)

start = time.time()
test2()
print("Time without numba.jit: ", time.time()-start)
