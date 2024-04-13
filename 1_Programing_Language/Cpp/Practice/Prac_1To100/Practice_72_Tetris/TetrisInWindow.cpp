#include "TetrisInWindow.h"

using TiW = TetrisInWindow;

TiW::TetrisInWindow(int rows, int cols, int leftMargin, int topMargin, int blockSize) : Tetris(rows, cols) {
    this->leftMargin = leftMargin;
    this->topMargin = topMargin;
    this->blockSize = blockSize;
    createWindow();
    initImage();
} 

TiW::TetrisInWindow() : TetrisInWindow(20, 10, 263, 133, 36) {
    createWindow();
    initImage();
}


void TiW::updateWindowFunc() {

    // draw background 
    drawBackground();

    // draw current block
    Point* points = curBlock->getPoints();
    for (int i = 0; i < 4; ++i) {
        drawBlock(points[i].row, points[i].col, curBlock->getType());
    }

    // draw solid blocks
    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < cols; ++col) {
            if (board[row][col] != EMPTY) {
                drawBlock(row, col, board[row][col]);
            }
        }
    }

    // draw next block
    points = nextBlock->getPoints();
    for (int i = 0; i < 4; ++i) {
        drawBlock(points[i].row, points[i].col + cols, nextBlock->getType());
    }

    std::string msg;
    // draw score
    msg = std::to_string(score);
    drawMsg(msg.c_str(), 670, 727);

    // draw speed level
    msg = std::to_string(curLevel + 1);
    drawMsg(msg.c_str(), 194, 727);

    // draw lines
    msg = std::to_string(eliminatedLines);
    drawMsg(msg.c_str(), 670, 817);

    // draw highest score
    msg = std::to_string(top10Scores[0]);
    drawMsg(msg.c_str(), 194, 817);

}

void TiW::initImage() {

    loadimage(&backgroundImg, "res/bg2.png");

    IMAGE blockImgs_Whole;
    loadimage(&blockImgs_Whole, "res/tiles.png");

    SetWorkingImage(&blockImgs_Whole);
    for (int i = 0; i < 7; ++i) {
        getimage(&blockImgs[i], i * blockSize, 0, blockSize, blockSize);
    }
    SetWorkingImage(nullptr);
}

void TiW::createWindow() {
    // create a window
    initgraph(938, 896);
}

void TiW::drawBackground() {
    putimage(0, 0, &backgroundImg);
}

void TiW::drawBlock(int row, int col, int blockType) {
    putimage(leftMargin + col * blockSize, topMargin + row * blockSize, &blockImgs[blockType]);
}

void TiW::drawMsg(const char *msg, int x, int y) {

    LOGFONT font;
    gettextstyle(&font);

    font.lfHeight = 60;
    font.lfWidth = 30;
    font.lfQuality = ANTIALIASED_QUALITY;
    strcpy_s(font.lfFaceName, sizeof(font.lfFaceName), _T("Consolas"));
    settextstyle(&font);

    setbkmode(TRANSPARENT);

    outtextxy(x, y, msg);

}