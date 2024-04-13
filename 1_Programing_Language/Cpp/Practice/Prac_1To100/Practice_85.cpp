#include <atomic>
#include <thread>
#include <iostream>

std::atomic<int> count = {0};

int main() {

    std::thread t1([]() {
        count.fetch_add(1);
    });

    std::thread t2([]() {
        count += 1;
        count += 1;
    });
    
    t1.join();
    t2.join();
    std::cout << count << std::endl;

    return 0;
}