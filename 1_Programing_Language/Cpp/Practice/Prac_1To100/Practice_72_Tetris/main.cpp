#include "TetrisInTerminal.h"
#include "TetrisInWindow.h"

#include <iostream>

int main() {

    std::cout << "1. Press 1 to play Tetris in terminal\n";
    std::cout << "2. Press 2 to play Tetris in window\n";

    int choice;
    std::cin >> choice;

    if (choice == 1) {
        TetrisInTerminal tetris;
        tetris.play();
    }
    else if (choice == 2) {
        TetrisInWindow tetris;
        tetris.play();
    }

    return 0;
}