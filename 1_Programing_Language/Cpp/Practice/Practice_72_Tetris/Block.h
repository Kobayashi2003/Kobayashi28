#pragma once

#include "Point.h"
#include <vector>
#include <cstdlib>

template <typename T>
using vv = std::vector<std::vector<T>>;

class Block {
public:
    Block();

    void initImages();

    /* move */
    // drop function: move the block down by 1 row each time
    void drop();
    // moveLeftRight function: move the block left or right by 1 column each time
    // direction = -1 or 1, means left or right
    void moveLeftRight(int direction);
    // rotate function: rotate 90 degrees anti-clockwise
    void rotate(); 
    
    /* the interface offered to the Tetris class */ 
    int getType();
    Point* getPoints();

    bool checkCollision(const vv<int> &board);
    void solidify(vv<int> &board);

    Block& operator=(const Block& other);

private:
    const int blocks[7][4] = {
        1, 3, 5, 7, // type 1
                    // 0 [1]
                    // 2 [3]
                    // 4 [5]
                    // 6 [7]

        2, 4, 5, 7, // type 2
                    //  0  1
                    // [2] 3
                    // [4][5]
                    //  6 [7]

        3, 4, 5, 6, // type 3
                    //  0  1
                    //  2 [3]
                    // [4][5]
                    // [6] 7

        3, 4, 5, 7, // type 4
                    //  0  1
                    //  2 [3]
                    // [4][5]
                    //  6 [7]
        
        2, 3, 5, 7, // type 5
                    //  0  1
                    // [2][3]
                    //  4 [5]
                    //  6 [7]

        3, 5, 6, 7, // type 6
                    //  0  1
                    //  2 [3]
                    //  4 [5]
                    // [6][7]

        2, 3, 4, 5, // type 7
                    //  0  1
                    // [2][3]
                    // [4][5]
                    //  6  7
    };
    int blockType; // 7 types of blocks
    Point blockPoints[4];

    static int blockWidth;
};