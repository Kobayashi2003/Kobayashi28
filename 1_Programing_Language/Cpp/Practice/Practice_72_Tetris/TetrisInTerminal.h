#pragma once

#include "Tetris.h"
#include <string>

class TetrisInTerminal : public Tetris {

public:
    TetrisInTerminal();
    TetrisInTerminal(int rows, int cols);

private:

    void loadConfig(); 

    virtual void updateWindowFunc();

    void getConsoleSize(); // TODO

    bool haveCurBlock(int row, int col);
    bool havePreBlock(int row, int col);

    void color(std::string str, int color);

private:

    int ConsoleWidth;
    int ConsoleHeight;
    int ConsoleWidthOld;
    int ConsoleHeightOld;

    Point *curBlockPoints;
    Point *preBlockPoints;
    int nextBlockType;

    char curBlock_icons[7] = { '#', '#', '#', '#', '#', '#', '#' };

    char background_icon = '.';
    char preBlock_icon = '@';

    bool showNextBlock = true;
    bool showPreBlock = true;
    bool showCurBlock = true;
    bool showBackground = true;
    bool showSolidBlock = true;
    bool showScore = true;
    bool showLevel = true;
    bool showLines = true;
    bool showTime = true;
    bool showSpeed = true;
    bool showHelp = true;

    bool COLOR = true;
    bool SOUND = true;

};