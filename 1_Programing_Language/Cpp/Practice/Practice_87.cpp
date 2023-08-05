#include <iostream>
#include <sstream>
#include <string>
#include <conio.h>
#include <thread>
#include <chrono>
// #include <mutex>
// #include <condition_variable>
// #include <future>
#include <atomic>
#include <cstdlib>
#include <ctime>
#include <windows.h>

int main() {

    // atomic width and height
    std::atomic<int> width = {0};
    std::atomic<int> height = {0};
    // get the size of console per 100 ms
    std::thread get_console_size([&]() {
        while (true) {
            CONSOLE_SCREEN_BUFFER_INFO csbi;
            GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi);
            width = csbi.srWindow.Right - csbi.srWindow.Left + 1;
            height = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    });

    // print a frame which just fit the console
    std::thread print_frame([&]() {
        int width_old = 0;
        int height_old = 0;
        while (true) {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000/60));

            // if the size of console is not changed, continue            
            if (width == width_old && height == height_old) {
                continue;
            }
            // clear the screen
            system("cls");
            // print the frame
            std::ostringstream frame;
            for (int i = 0; i < height; ++i) {
                for (int j = 0; j < width; ++j) {
                    if (i == 0 || i == height - 1) {
                        frame << "*";
                    } else if (j == 0 || j == width - 1) {
                        frame << "*";
                    } else {
                        frame << " ";
                    }
                }
                if (i != height - 1) {
                    frame << std::endl;
                }
            }
            
            std::string frame_str = frame.str();
            // add a KOBAYASHI in the middle, and randomly change the color
            std::srand(std::time(nullptr));
            int color = std::rand() % 15 + 1;
            int pos = (height / 2) * (width + 1) + (width / 2) - 4;
            frame_str.replace(pos, 9, "\033[3" + std::to_string(color) + "mKOBAYASHI\033[0m");
            std::cout << frame_str;
            

            // update the old width and height
            width_old = width;
            height_old = height;
        }
    });

    // wait for the user to press any key
    _getch();

    // end the thread when main thread is ended
    get_console_size.detach();
    print_frame.detach();

    return 0;
}
