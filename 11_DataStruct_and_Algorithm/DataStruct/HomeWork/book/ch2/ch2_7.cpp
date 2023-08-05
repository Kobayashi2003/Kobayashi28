#include <iostream>
#include <ctime>

void test1(size_t n) { // O(n)
    clock_t start = clock();
    size_t sum = 0;
    for (size_t i = 0; i < n; ++i) 
        ++sum;
    clock_t end = clock();
    std::cout << "test1: " << (double)(end - start) / CLOCKS_PER_SEC << "s" << std::endl;
}


void test2(size_t n) { // O(n^2)
    clock_t start = clock();
    size_t sum = 0;
    for (size_t i = 0; i < n; ++i) 
        for (size_t j = 0; j < n; ++j) 
            ++sum;
    clock_t end = clock();
    std::cout << "test2: " << (double)(end - start) / CLOCKS_PER_SEC << "s" << std::endl;
}


void test3(size_t n) { // O(n^3)
    clock_t start = clock();
    size_t sum = 0;
    for (size_t i = 0; i < n; ++i) 
        for (size_t j = 0; j < n*n; ++j) 
            ++sum;
    clock_t end = clock();
    std::cout << "test3: " << (double)(end - start) / CLOCKS_PER_SEC << "s" << std::endl;
}


void test4(size_t n) { // O(n^2)
    clock_t start = clock();
    size_t sum = 0;
    for (size_t i = 0; i < n; ++i) 
        for (size_t j = 0; j < i; ++j) 
            ++sum;
    clock_t end = clock();
    std::cout << "test4: " << (double)(end - start) / CLOCKS_PER_SEC << "s" << std::endl;
}


void test5(size_t n) { // O(n^5)
    clock_t start = clock();
    size_t sum = 0;
    for (size_t i = 0; i < n; ++i) 
        for (size_t j = 0; j < i*i; ++j) 
            for (size_t k = 0; k < j; ++k) 
                ++sum;
    clock_t end = clock();
    std::cout << "test5: " << (double)(end - start) / CLOCKS_PER_SEC << "s" << std::endl;
}


void test6(size_t n) { // O(n^4)
    clock_t start = clock();
    size_t sum = 0;
    for (size_t i = 0; i < n; ++i) 
        for (size_t j = 0; j < i*i; ++j) 
            if (j % i == 0)
                for (size_t k = 0; k < j; ++k) 
                    ++sum;
    clock_t end = clock();
    std::cout << "test6: " << (double)(end - start) / CLOCKS_PER_SEC << "s" << std::endl;
}

void test(void func(size_t), long long int n) {
    for (int i = 0; i < 15; ++i)
        func((size_t)n * (i + 1));
}


int main() {

    test(test1, 1e8);
    test(test2, 1e4);
    test(test3, 1e2);
    test(test4, 1e4);
    test(test5, 50);
    test(test6, 1e2);

    return 0; 
}