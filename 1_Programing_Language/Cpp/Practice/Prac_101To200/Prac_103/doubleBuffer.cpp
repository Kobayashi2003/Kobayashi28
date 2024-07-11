#include <iostream>
#include <random>
#include <vector>
#include <thread>
#include <chrono>

#include <Windows.h>
#include <conio.h>


enum DIRECTION { UP, DOWN, LEFT, RIGHT };
DIRECTION direction = RIGHT;

void capture_input() {
    while (1) {
        if (!_kbhit()) {
            continue;
        }
        char input = _getch();
        switch (input) {
        case 'w':
            if (direction == DOWN) break;
            direction = UP; break;
        case 's':
            if (direction == UP) break;
            direction = DOWN; break;
        case 'a':
            if (direction == RIGHT) break;
            direction = LEFT; break;
        case 'd':
            if (direction == LEFT) break;
            direction = RIGHT; break;
        default:
            break;
        }
    }
}


int main() {

    // get the default standard output buffer handle
    COORD coord = { 0, 0 };
    HANDLE hOutPut = GetStdHandle(STD_OUTPUT_HANDLE);

    // create a new console screen buffer
    HANDLE hOutBuf = CreateConsoleScreenBuffer(
        GENERIC_READ | GENERIC_WRITE,       // Desired access   
        FILE_SHARE_READ | FILE_SHARE_WRITE, // Share mode 
        NULL,                               // Security attributes 
        CONSOLE_TEXTMODE_BUFFER,            // Screen buffer size
        NULL                                // Default buffer size
    );

    // set the new console screen buffer as the active screen buffer
    SetConsoleActiveScreenBuffer(hOutBuf);

    // hide the two console screen buffer's cursor
    CONSOLE_CURSOR_INFO cci;
    cci.bVisible = 0;
    cci.dwSize = 1;
    SetConsoleCursorInfo(hOutPut, &cci);
    SetConsoleCursorInfo(hOutBuf, &cci);

    // create a thread to capture user input
    std::thread input_thread(capture_input);


    char width = 10;
    char height = 10;

    char snake_length = 3;
    bool snake_alive = true;
    
    std::vector<char> snake_x;
    std::vector<char> snake_y;
    
    for (int i = 0; i < snake_length; i++) {
        snake_x.push_back(width / 2 + i * (direction == LEFT) - i * (direction == RIGHT));
        snake_y.push_back(height / 2 + i * (direction == UP) - i * (direction == DOWN));
    }

    char food_x;
    char food_y;

    while (snake_alive) {

        // update snake position based on user input
        snake_x.insert(snake_x.begin(), snake_x[0] - (direction == LEFT) + (direction == RIGHT));
        snake_y.insert(snake_y.begin(), snake_y[0] - (direction == UP) + (direction == DOWN));
        // generate new food position if the snake eats the food
        if (food_x == snake_x[0] && food_y == snake_y[0]) {
            food_x = rand() % width;
            food_y = rand() % height;
            snake_length++;
        } else { 
            snake_x.pop_back();
            snake_y.pop_back();
        }

        // // check for collision with walls or itself
        if (snake_x[0] < 0 || snake_x[0] >= width || snake_y[0] < 0 || snake_y[0] >= height) {
            snake_alive = false;
        }

        for (int i = 1; i < snake_length; i++) {
            if (snake_x[0] == snake_x[i] && snake_y[0] == snake_y[i]) {
                snake_alive = false;
            }
        }

        // clear the console screen buffer
        system("cls");

        // display snake
        for (int i = 0; i < snake_length; i++) {
            SetConsoleCursorPosition(hOutBuf, { snake_x[i], snake_y[i] });
            std::cout << "*";
        }

        // display food
        SetConsoleCursorPosition(hOutBuf, { food_x, food_y });
        std::cout << "O";

        // swap the console screen buffers
        SetConsoleActiveScreenBuffer(hOutBuf);
        hOutBuf = hOutPut;
        hOutPut = GetStdHandle(STD_OUTPUT_HANDLE);

        // delay for a short time
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }

    // game over
    std::cout << "Game Over!";
    return 0;
}