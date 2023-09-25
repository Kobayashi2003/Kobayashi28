#include "TypingPractice.h"
#include <string>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <iostream>
#include <conio.h>
#include <thread>
#include <chrono>
#include <fstream>

VS WORDLIST = { // key words of C++11
    "asm", "auto", "bool", "break", "case",
    "catch", "char", "class", "const", "const_cast",
    "continue", "default", "delete", "do", "double",
    "dynamic_cast", "else", "enum", "explicit", "export",
    "extern", "false", "float", "for", "friend",
    "goto", "if", "inline", "int", "long",
    "mutable", "namespace", "new", "operator", "private",
    "protected", "public", "register", "reinterpret_cast", "return",
    "short", "signed", "sizeof", "static", "static_cast",
    "struct", "switch", "template", "this", "throw",
    "true", "try", "typedef", "typeid", "typename",
    "union", "unsigned", "using", "virtual", "void",
    "volatile", "wchar_t", "while"   
};

void TypingPractice::KOBAYASHI() {
    system("cls");
    std::string str = "Welcome to KOBAYASHI's typing practice!";
    for (auto c : str) {
        std::cout << c;
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
    std::cout << std::endl;
    // clear screen
    // std::cout << "\033[2J\033[1;1H";
    std::cout << "Press any key to continue..." << std::endl;
    std::cin.get();
    system("cls");
}

TypingPractice::TypingPractice(int wordNumber, int timeLimit, int mistakeLimit) {
    this->wordNumber = wordNumber;
    this->timeLimit = timeLimit;
    this->mistakeLimit = mistakeLimit;
}

VS TypingPractice::wordList = WORDLIST;

void TypingPractice::getConsoleWidth() {
    while (1) {
        // the width of the console window is save in the first line of the ConsoleSize
        std::ifstream file("ConsoleSize");
        file >> ConsoleWidth;
        file.close();
        // every 0.1 second, check the width of the console window
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

void TypingPractice::checkConsoleWidth() {
    while (1) {
        if (ConsoleWidthOld == 0) {
            ConsoleWidthOld = ConsoleWidth;
        }
        else if (ConsoleWidth != ConsoleWidthOld) {
            ConsoleWidthOld = ConsoleWidth;
            update();  
        } 
        // every 0.1 second, check the width of the console window
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

void TypingPractice::update() {
    // if last update is less than 0.3 second ago, ignore this update
    if (lastUpdate + 300 > clock()) {
        return;
    }
    system("cls");
    showPracticeText(showQuick); 
    lastUpdate = clock();
}

void TypingPractice::play() {

    // init the data
    init();

    // use multi-thread to monitor the width of the console window
    std::thread t_GCW(&TypingPractice::getConsoleWidth, this);
    std::thread t_CCW(&TypingPractice::checkConsoleWidth, this);

    // Print practice text
    showPracticeText();

    // Input monitor
    inputMonitor();

    // Print result
    if (isEnd) {
        printResult();
        t_GCW.detach();
        t_CCW.detach();
    }
}

void TypingPractice::init() {
    // Clear screen
    // std::cout << "\033[2J\033[1;1H";
    system("cls");
    // Seed random number generator
    srand(time(nullptr));
    // Generate practice text randomly
    int countWord = 0;
    practiceText = "";
    while (countWord < wordNumber) {
        // randomly choose a word from wordList
        int index = rand() % wordList.size();
        practiceText += wordList[index];
        if (countWord < wordNumber - 1) {
            practiceText += " ";
        }
        countWord += 1;
    }
    textLength = practiceText.length();
    isStart = false;
    isEnd = false;
    countMistake = 0;
    speed = .0;

    ConsoleWidth = 0;
    ConsoleWidthOld = 0;

    lastUpdate = 0;
}

void TypingPractice::showPracticeText(int showSpeed) {
    // Print practice text
    // std::cout << practiceText << std::endl;
    int count = 0;
    for (auto ch : practiceText) {
        if (count == ConsoleWidth - 1) {
            break;
        }
        std::cout << ch; count += 1;
        // small special delay to make it look like a real typing (over in 3 seconds)
        std::this_thread::sleep_for(std::chrono::milliseconds(showSpeed / practiceText.length()));
    }
    // back to the top
    for (int i = 0; i < count; ++i) {
        std::cout << "\b";
    }
}

void TypingPractice::inputMonitor() {
    int count = 0;
    while (!isEnd) {
        char ch = '\0';
        if (_kbhit()) {
            if (!isStart) { // if the first character is input, start the timer
                startTime = time(nullptr);
                isStart = true;
            }
            ch = _getch();
            if (ch == practiceText[0]) {
                practiceText.erase(0, 1);
                std::cout << " ";
                count += 1;
            }
            else {
                errorPrompt();
            }
        }
        if (count == ConsoleWidth - 1) { // the last character of this line
            count = 0;
            update();
        }
        if (practiceText.length() == 0) { // when the practice text is empty, set the end time and end the loop
            endTime = time(nullptr);
            isEnd = true;
        }
    }
}

void TypingPractice::errorPrompt() {
    std::cout << "\a";
    countMistake += 1;
}

void TypingPractice::printResult() {
    if (mistakeLimit != 0 && countMistake > mistakeLimit) {
        result = false;
    }
    else if (timeLimit != 0 && endTime - startTime > timeLimit) {
        result = false;
    }
    else {
        result = true;
    }

    // clear screen
    // std::cout << "\033[2J\033[1;1H";
    system("cls");

    if (result) {
        std::cout << "You win!" << std::endl;
    } else {
        std::cout << "You lose!" << std::endl;
    }

    // Print the detail of the result
    std::cout << "Time: " << endTime - startTime << "s" << std::endl;
    std::cout << "Mistake: " << countMistake << std::endl;
    // kpm
    std::cout << "Speed: " << (textLength - countMistake) / (endTime - startTime) * 60 << "kpm" << std::endl;

    // create a file named "ENDFLAG" to indicate the end of the game
    std::ofstream file("ENDFLAG");
    file.close();
}
