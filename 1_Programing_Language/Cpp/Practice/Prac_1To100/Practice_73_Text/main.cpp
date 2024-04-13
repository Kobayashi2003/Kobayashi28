#include "Text.h"
#include <iostream>

void showMenu() {
    std::cout << "1. Show text" << std::endl;
    std::cout << "2. Find string" << std::endl;
    std::cout << "3. Set path" << std::endl;
    std::cout << "4. Exit" << std::endl;
}

int main() {
    std::cout << "please enter the path to the file: ";
    std::string path;
    std::getline(std::cin, path);
    Text text(path);

    int choice = 0;
    while (choice != 4) {
        showMenu();
        std::cin >> choice;
        std::cin.ignore();
        if  (choice == 1) {
            text.showText();
        }
        else if (choice == 2) {
            std::cout << "please enter the string: ";
            std::string str;
            std::getline(std::cin, str);
            auto result = text.find(str);
            std::cout << result[0] << std::endl;
            std::cout << "line: " << result[1] << std::endl;
        }
        else if (choice == 3) {
            std::cout << "please enter the path to the file: ";
            std::string path;
            std::getline(std::cin, path);
            text.setPath(path); 
        }    
        else if (choice == 4) {
            std::cout << "Goodbye" << std::endl;
        }
        else {
            std::cout << "Wrong input" << std::endl;
        }
    }
    return 0;
}