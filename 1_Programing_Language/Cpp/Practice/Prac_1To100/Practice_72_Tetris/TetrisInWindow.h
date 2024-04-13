#include "Tetris.h"
#include <graphics.h>
 

class TetrisInWindow : public Tetris {
public:
    TetrisInWindow();
    TetrisInWindow(int rows, int cols, int leftMargin, int topMargin, int blockSize);

private:

    virtual void updateWindowFunc();

    void initImage();

    void createWindow();
    void drawBackground();
    void drawBlock(int row, int col, int blockType);
    void drawMsg(const char* msg, int x, int y);

private:

    int leftMargin;
    int topMargin;
    int blockSize;

    IMAGE blockImgs[7];
    IMAGE backgroundImg;

};