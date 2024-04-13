#include <atomic>
#include <iostream>

struct A {
    float x;
    int y;
    long long z;
};


int main() {
    std::atomic<A> a;
    std::cout << std::boolalpha << a.is_lock_free() << std::endl;
    // undefined reference to `__atomic_is_lock_free'
    return 0;
}