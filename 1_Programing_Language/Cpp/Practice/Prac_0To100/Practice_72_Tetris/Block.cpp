#include "Block.h"

int Block::blockWidth = 36;

Block::Block() {

    initImages();

    // randomly choose a type of block  
    blockType = rand() % 7;

    // set the coordinates of the 4 points of the block
    for (int i = 0; i < 4; ++i) {
        // default: the block will be placed at the left top corner of the board
        blockPoints[i].row = blocks[blockType][i] / 2;
        blockPoints[i].col = blocks[blockType][i] % 2; 
    }
}

void Block::initImages() { // TODO

}

void Block::drop() { // done
    for (auto &point :blockPoints) {
        point.row += 1;
    }
}

void Block::moveLeftRight(int direction) { // done
    // direction = -1 or 1, means left or right
    for (auto &point : blockPoints) {
        point.col += direction;
    }
}

void Block::rotate() { // done
    // rotate 90 degrees anti-clockwise
    Point center = blockPoints[1];
    for (auto &point : blockPoints) {
        int row = point.row - center.row;
        int col = point.col - center.col;
        point.row = center.row - col;
        point.col = center.col + row;
    }
}

int Block::getType() { // done
    return blockType;
}

Point* Block::getPoints() { // done
    return blockPoints;
}

bool Block::checkCollision(const vv<int> &board) { // done
    int rows = board.size();
    int cols = board[0].size();
    for (auto &point : blockPoints) {
        if (point.col < 0 || point.col >= cols ||
            point.row < 0 || point.row >= rows ||
            board[point.row][point.col] != -1) {
                return true;
        }
    }
    return false;
}

void Block::solidify(vv<int> &board) { // done
    // solidify means to set the value of the board to the type of the block
    for (auto &point : blockPoints) {
        board[point.row][point.col] = blockType;
    }
}

Block& Block::operator=(const Block& other) { // done
    if (this == &other) {
        return *this;
    }

    this->blockType = other.blockType;

    for (int i = 0; i < 4; ++i) {
        this->blockPoints[i] = other.blockPoints[i];
    }

    return *this;
}