#include "TetrisInTerminal.h"


using TiT = TetrisInTerminal;

TiT::TetrisInTerminal(int rows, int cols) : Tetris(rows, cols) { loadConfig(); }

TiT::TetrisInTerminal() : TetrisInTerminal(20, 10) {}


void TiT::loadConfig() {
    // load config from "titconfig" file
    std::ifstream fin("titconfig");
    if (!fin.is_open()) {
        // if the file is not exist, create it, and write the default config 
        std::ofstream fout("titconfig");
        fout << "curBlock_icons = #######" << std::endl;
        fout << "background_icon = ." << std::endl;
        fout << "preBlock_icon = @" << std::endl;

        fout << "showNextBlock = true" << std::endl;
        fout << "showPreBlock = true" << std::endl;
        fout << "showCurBlock = true" << std::endl;
        fout << "showBackground = true" << std::endl;
        fout << "showSolidBlock = true" << std::endl;
        fout << "showScore = true" << std::endl;
        fout << "showLevel = true" << std::endl;
        fout << "showLines = true" << std::endl;
        fout << "showTime = true" << std::endl;
        fout << "showSpeed = true" << std::endl;
        fout << "showHelp = true" << std::endl;

        fout << "COLOR = true" << std::endl;
        fout << "SOUND = true" << std::endl;
    }

    else {
        // load the config from the file
        std::string str;
        while (fin >> str) {
            if (str == "curBlock_icons") {
                fin >> str; fin >> str;
                for (int i = 0; i < 7; ++i) {
                    curBlock_icons[i] = str[i];
                }
            } else if (str == "background_icon") {
                fin >> str; fin >> str;
                background_icon = str[0];
            } else if (str == "preBlock_icon") {
                fin >> str; fin >> str;
                preBlock_icon = str[0];
            } else if (str == "showNextBlock") {
                fin >> str; fin >> str;
                showNextBlock = (str == "true");
            } else if (str == "showPreBlock") {
                fin >> str; fin >> str;
                showPreBlock = (str == "true");
            } else if (str == "showCurBlock") {
                fin >> str; fin >> str;
                showCurBlock = (str == "true");
            } else if (str == "showBackground") {
                fin >> str; fin >> str;
                showBackground = (str == "true");
            } else if (str == "showSolidBlock") {
                fin >> str; fin >> str;
                showSolidBlock = (str == "true");
            } else if (str == "showScore") {
                fin >> str; fin >> str;
                showScore = (str == "true");
            } else if (str == "showLevel") {
                fin >> str; fin >> str;
                showLevel = (str == "true");
            } else if (str == "showLines") {
                fin >> str; fin >> str;
                showLines = (str == "true");
            } else if (str == "showTime") {
                fin >> str; fin >> str;
                showTime = (str == "true");
            } else if (str == "showSpeed") {
                fin >> str; fin >> str;
                showSpeed = (str == "true");
            } else if (str == "showHelp") {
                fin >> str; fin >> str;
                showHelp = (str == "true");
            } else if (str == "COLOR") {
                fin >> str; fin >> str;
                COLOR = (str == "true");
            } else if (str == "SOUND") {
                fin >> str; fin >> str;
                SOUND = (str == "true");
            } else {
                std::cerr << "Error: unknown config: " << str << std::endl;
            }
        }
    }
}

void TiT::updateWindowFunc() {
    // clear the screen 
    std::cout << "\033[2J\033[1;1H"; // system("cls");

    curBlockPoints = curBlock->getPoints();
    preBlockPoints = preBlock.getPoints();
    nextBlockType = nextBlock->getType();

    // travel the board and print the blocks
    for (int row = 0; row < rows; ++row) {
        // show the board
        for (int col = 0; col < cols; ++col) {
            bool haveCur = haveCurBlock(row, col);
            bool havePre = havePreBlock(row, col);
            if (showCurBlock && haveCur) {
                if (COLOR) {
                    color(std::string("") + curBlock_icons[curBlock->getType()], curBlock->getType());
                } else {
                    std::cout << curBlock->getType();
                }
            } else if (showCurBlock && havePre) {
                if (COLOR) {
                    color(std::string("") + preBlock_icon, preBlock.getType());
                } else {
                    std::cout << preBlock_icon;
                }
            } else {
                if (showBackground && board[row][col] == EMPTY) {
                    if (COLOR) {
                        color(std::string("") + background_icon, -1);
                    } else {
                        std::cout << background_icon;
                    }
                } else if (showSolidBlock && board[row][col] != EMPTY) {
                    if (COLOR) {
                        color(std::string("") + curBlock_icons[board[row][col]], board[row][col]);
                    } else {
                        std::cout << board[row][col];
                    }
                }
            }
        }

        // show the next block
        if (showNextBlock) {
            if (row == 0) {
                std::cout << "\t\tNext Block:";
            }
            else if (row == 1) {
                std::cout << "\t\t";
                switch (nextBlockType) {
                default:
                    std::cout << " " << 0 << " ";
                    break;
                }
                switch (nextBlockType) {
                case 0: 
                    if (COLOR) {
                        color("[", nextBlockType);
                        std::cout << "1";
                        color("]", nextBlockType);
                        break;
                    }
                    std::cout << "[" << 1 << "]"; break;
                default:
                    std::cout << " " << 1 << " "; break;
                }
            }
            else if (row == 2) {
                std::cout << "\t\t";
                switch (nextBlockType) {
                case 1: case 4: case 6:
                    if (COLOR) {
                        color("[", nextBlockType);
                        std::cout << "2";
                        color("]", nextBlockType);
                        break;
                    }
                    std::cout << "[" << 2 << "]"; break;
                default:
                    std::cout << " " << 2 << " "; break;
                }
                switch (nextBlockType) {
                case 0: case 2: case 3: case 4: case 5: case 6:
                    if (COLOR) {
                        color("[", nextBlockType);
                        std::cout << "3";
                        color("]", nextBlockType);
                        break;
                    }
                    std::cout << "[" << 3 << "]"; break;
                default:
                    std::cout << " " << 3 << " "; break;
                }
            }
            else if (row == 3) {
                std::cout << "\t\t";
                switch (nextBlockType) {
                case 1: case 2: case 3: case 6:
                    if (COLOR) {
                        color("[", nextBlockType);
                        std::cout << "4";
                        color("]", nextBlockType);
                        break;
                    }
                    std::cout << "[" << 4 << "]"; break;
                default:
                    std::cout << " " << 4 << " "; break;
                }
                switch (nextBlockType) {
                case 0: case 1: case 2: case 3: case 4: case 5: case 6:
                    if (COLOR) {
                        color("[", nextBlockType);
                        std::cout << "5";
                        color("]", nextBlockType);
                        break;
                    }
                    std::cout << "[" << 5 << "]"; break;
                default:
                    std::cout << " " << 5 << " "; break;
                }
            }
            else if (row == 4) {
                std::cout << "\t\t";
                switch (nextBlockType) {
                case 2: case 5:
                    if (COLOR) {
                        color("[", nextBlockType);
                        std::cout << "6";
                        color("]", nextBlockType);
                        break;
                    }
                    std::cout << "[" << 6 << "]"; break;
                default:
                    std::cout << " " << 6 << " "; break;
                }
                switch (nextBlockType) {
                case 0: case 1: case 3: case 4: case 5:
                    if (COLOR) {
                        color("[", nextBlockType);
                        std::cout << "7";
                        color("]", nextBlockType);
                        break;
                    }
                    std::cout << "[" << 7 << "]"; break;
                default:
                    std::cout << " " << 7 << " "; break;
                }
            }
        }

        // show the score, level, time, speed
        if (showScore && row == 7) {
            std::cout << "\t\tScore: " << score;
        }
        if (showLevel && row == 8) {
            std::cout << "\t\tLevel: " << curLevel;
        }
        if (showTime && row == 9) {
            std::cout << "\t\tTime: " << gameTime;  
        }
        if (showSpeed && row == 10) {
            std::cout << "\t\tSpeed: " << speed;
        }
        if (showLines && row == 11) {
            std::cout << "\t\tLines: " << eliminatedLines;
        }
        std::cout << std::endl;
    }
    
    // show the help
    if (showHelp) {
        std::cout << "\n\n\
        \t\t'A' 'LEFT' move left\n\
        \t\t'D' 'RIGHT' move right\n\
        \t\t'W' 'UP' rotate\n\
        \t\t'S' 'DOWN' drop speedup\n\
        \t\t'SPACE' droop\n\
        \t\t'P' pause\n\
        \t\t'Q' 'ESC' quit\n";
    }
}

void TiT::getConsoleSize() {
    // TODO
}

bool TiT::haveCurBlock(int row, int col) {
    for (int i = 0; i < 4; ++i) {
        if (curBlockPoints[i].row == row && curBlockPoints[i].col == col) {
            return true;
        }
    }
    return false;
}

bool TiT::havePreBlock(int row, int col) {
    for (int i = 0; i < 4; ++i) {
        if (preBlockPoints[i].row == row && preBlockPoints[i].col == col) {
            return true;
        }
    }
    return false;
}

void TiT::color(std::string str, int color) {
    // -1 : black   0 : red    1 : green
    // 2 : yellow   3 : blue   4 : purple
    // 5 : cyan     6 : orange 7 : white
    switch (color) {
        case -1: std::cout << "\033[30m"; break;
        case 0: std::cout << "\033[31m"; break;
        case 1: std::cout << "\033[32m"; break;
        case 2: std::cout << "\033[33m"; break;
        case 3: std::cout << "\033[34m"; break;
        case 4: std::cout << "\033[35m"; break;
        case 5: std::cout << "\033[36m"; break;
        case 6: std::cout << "\033[33m"; break;
        case 7: std::cout << "\033[37m"; break;
        default: std::cout << "\033[37m"; break;
    }
    std::cout << str << "\033[0m";
}
