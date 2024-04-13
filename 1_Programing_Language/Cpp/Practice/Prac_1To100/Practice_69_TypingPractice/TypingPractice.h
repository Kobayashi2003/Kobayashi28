#include <vector>
#include <string>

using VS = std::vector<std::string>;



// TypingPractice.h
class TypingPractice {
public:
    TypingPractice(int wordNumber, int timeLimit=0, int mistakeLimit=0);
    void play();

    static void KOBAYASHI();

private:

    void getConsoleWidth();
    void checkConsoleWidth();
    void update();

    void init();
    void showPracticeText(int showSpeed=showSlow);
    void inputMonitor();
    void errorPrompt();
    void printResult();
    
private:

    int ConsoleWidth;
    int ConsoleWidthOld;

    int wordNumber;
    int timeLimit;
    int mistakeLimit;
    static VS wordList;
    std::string practiceText;
    int textLength;

    bool isStart;
    bool isEnd;
    time_t startTime;
    time_t endTime;

    int countMistake;
    double speed;

    constexpr static int showSlow = 800;
    constexpr static int showQuick = 100;

    int lastUpdate;

    bool result; // true: WIN, false: LOSE
};