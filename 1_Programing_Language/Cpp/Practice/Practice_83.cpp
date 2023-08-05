#include <thread>
#include <chrono>
#include <iostream>

int main() {

    std::thread::id main_thread_id = std::this_thread::get_id();
    std::cout << "main_thread_id: " << main_thread_id << std::endl;

    auto say_hello = [&]() {
        std::cout << "Hello" << std::endl;
    };
    auto say_world = [&]() {
        std::cout << "World" << std::endl;
    };

    std::thread t1(say_hello);
    std::thread t2(say_world);

    auto start = std::chrono::system_clock::now();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double, std::milli> elapsed = end - start;
    std::cout << "Waited " << elapsed.count() << " ms\n";


    std::cout << "t1_id: " << t1.get_id() << std::endl;
    std::cout << "t2_id: " << t2.get_id() << std::endl;

    std::swap(t1, t2);

    std::cout << "t1_id: " << t1.get_id() << std::endl;
    std::cout << "t2_id: " << t2.get_id() << std::endl;

    std::cout << t1.hardware_concurrency() << std::endl;
    std::cout << t1.joinable() << std::endl;
    t1.join();

    return 0;   
}