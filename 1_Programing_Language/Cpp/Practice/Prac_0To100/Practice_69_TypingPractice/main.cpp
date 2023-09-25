#include "TypingPractice.h"
#include <iostream>

int main() {
    while (1) {
        TypingPractice::KOBAYASHI();
        std::cout << "Please input the number of words you want to practice: ";
        int wordNumber = 0; std::cin >> wordNumber;
        TypingPractice tp(wordNumber);
        tp.play();

        std::cout << "Do you want to continue? (y/n): ";
        char c; std::cin >> c;
        if (c == 'y' || c == 'Y') {
            continue;
        } else {
            break;
        }
    }
    return 0;
}