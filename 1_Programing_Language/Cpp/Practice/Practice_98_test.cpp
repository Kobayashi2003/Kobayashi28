#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <atomic>

using namespace std;

// int n = 0;
atomic<int> n(0);
std::mutex m;

void increase_number() {
    for (int i = 0; i < 1e6; ++i) {
        // m.lock();
        ++n;
        // m.unlock();
    }
}

int main() {

    vector<thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.push_back(thread(increase_number));
    }

    for (auto& th : threads) {
        th.join();
    }

    cout << n << endl;

    return 0;
}