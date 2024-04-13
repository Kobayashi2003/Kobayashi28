#include <queue>
#include <chrono>
#include <mutex>
#include <thread>
#include <iostream>
#include <condition_variable>

int main() {
    std::queue<int> produced_nums;
    std::mutex mtx;
    std::condition_variable cv;
    bool notified = false; // notification flag

    // producer thread
    auto producer = [&]() {
        for (int i = 0; ; i++) {
            std::this_thread::sleep_for(std::chrono::seconds(5));
            std::unique_lock<std::mutex> lock(mtx);
            std::cout << "producing " << i << std::endl;
            produced_nums.push(i);
            notified = true;
            cv.notify_all(); // notify_one() can be used here
        }
    };

    // consumer thread
    auto consumer = [&]() {
        while (true) {
            std::unique_lock<std::mutex> lock(mtx);
            while (!notified) { // avoid spurious wakeups
                cv.wait(lock);
            }
            // unlock for a while
            lock.unlock();
            std::this_thread::sleep_for(std::chrono::seconds(1));
            lock.lock();
            while (!produced_nums.empty()) {
                std::cout << "consuming " << produced_nums.front() << std::endl;
                produced_nums.pop();
            }
            notified = false;
        }        
    }; 

    std::thread p(producer);
    std::thread cs[2];
    for (int i = 0; i < 2; i++) {
        cs[i] = std::thread(consumer);
    }
    p.join();
    for (int i = 0; i < 2; i++) {
        cs[i].join();
    }
    
    return 0;
}