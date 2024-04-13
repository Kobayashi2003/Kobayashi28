#include <iostream>
#include <future>
#include <thread>

int main() {
    // 将是一个返回值为 7 的 lambda 表达式封装到 task 中
    // std::packaged_task 的模板参数为要封装函数的类型
    std::packaged_task<int()> task([]() {return 7;});
    // 获得 tack 的期物
    std::future<int> result = task.get_future(); // 在一个线程中执行 task
    std::thread(std::move(task)).detach();
    std::cout << "waiting...";
    result.wait(); // 在此设置屏障，阻塞到期物的完成
    std::cout << "done!" << std::endl << "result is " << result.get() << std::endl;
    return 0;
}