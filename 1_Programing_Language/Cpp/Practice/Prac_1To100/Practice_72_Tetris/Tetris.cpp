#include "Tetris.h"

void Tetris::initDescription() { // done
    gameName = "Tetris";
    gameVersion = "1.0";
    gameAuthor = "KOBAYASHI";
}

void Tetris::showDescription() { // done
    std::cout << "Game Name: " << gameName << std::endl;
    std::cout << "Game Version: " << gameVersion << std::endl;
    std::cout << "Game Author: " << gameAuthor << std::endl;
}


Tetris::Tetris(int rows, int cols)  { // done
    this->rows = rows;
    this->cols = cols;
}

Tetris::~Tetris() { // done
    delete curBlock;
    delete nextBlock;
}


void Tetris::play() { // done

    init();
    
    // create the first block
    nextBlock = new Block();
    curBlock = nextBlock;
    nextBlock = new Block();
    createPreBlock();

    startTime = clock();

    // create a thread to update the time in Tetris
    auto UpdateTime = [&]() {
        while (gameStart) {
            lock_updateTimer = false;
            updateTimer();
            lock_updateTimer = true;
        }
    };
    std::thread t_time(UpdateTime);
    p_t_updateTimer = &t_time;

    // create a thread to accept the key event
    auto KeyEvent = [&]() {
        while (gameStart) {
            lock_keyEvent = false;
            checkPause();
            keyEvent();
            lock_keyEvent = true;
        }
    };
    std::thread t_key(KeyEvent);
    p_t_keyEvent = &t_key;

    // create a thread to control the drop of the curBlock
    auto DropBlock = [&]() {
        while (gameStart) {
            lock_dropBlock = false;
            checkPause();
            std::this_thread::sleep_for(std::chrono::milliseconds(curSpeed - speedUp));
            drop();
            speedUp = 0;
            lock_dropBlock = true;
        }
    };
    std::thread t_drop(DropBlock);
    p_t_dropBlock = &t_drop;

    // create a thread to control the preview of the curBlock
    auto CreatePreBlock = [&]() {
        while (gameStart) {
            lock_createPreBlock = false;
            checkPause();
            int c_0col = curBlock->getPoints()[0].col;
            int p_0col = preBlock.getPoints()[0].col;
            int c_3col = curBlock->getPoints()[3].col;
            int p_3col = preBlock.getPoints()[3].col;

            if (preBlock.checkCollision(board) || c_0col != p_0col || c_3col != p_3col) {
                createPreBlock();
            }

            lock_createPreBlock = true;
        }
    };
    std::thread t_pre(CreatePreBlock);

    // the main loop of the game, mainly used to check the update flags and game state flags
    for (; gameStart; delay_fps(60)) {
        
        if (updateWindowFlag) {
            updateWindowFunc();
            updateWindowFlag = false;
        }

        if (updateScoreLevelFlag) {
            updateScore();
            updateLevel();
            updateScoreLevelFlag = false;
        }
       
        if (gamePause) {
            std::cout << "Press 'P' to continue the game" << std::endl;
            // pause the game
            while (gamePause) {
                keyEvent();
            }
        }

        if (gameOver) {
            std::cout << "You lose!" << std::endl;
            gameStart = false;

        } else if (gameWin) {
            std::cout << "You win!" << std::endl;
            gameStart = false;
        }

        if (!gameStart) {
            // release the threads
            t_time.join();
            t_key.join();
            t_drop.join();
            t_pre.join();

            // update the file
            updateTop10ScoresFile();
            updateHistoryFile();

            // 'q' to quit the game
            // 'r' to restart the game

            std::cout << "[q] to quit the game" << std::endl;
            std::cout << "[r] to restart the game" << std::endl;
            char c;
            std::cin >> c;
            if (c == 'r') {
                break;
            } else {
                return;
            }
        }
    }
}

void Tetris::init() { // done

    // init the description
    initDescription();

    // set the random seed
    srand((unsigned)time(nullptr));
    curBlock = nullptr;
    nextBlock = nullptr;

    // init the board
    clearBoard();

    // init the game state flags
    gameStart = true;
    gameOver = false;
    gamePause = false;
    gameWin = false;

    // init the function flags
    updateWindowFlag = false;
    updateScoreLevelFlag = false;

    // init the game status
    eliminatedLines = 0;
    combo = 0;
    score = 0;
    curLevel = EASY;
    curSpeed = speed[curLevel];
    speedUp = 0;

    // init the top 10 scores
    top10Scores = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    loadTop10Scores();
}

void Tetris::clearBoard() { // done
    // clear all the elements in the Board
    board.clear();
    // reset the Board
    for (int i = 0; i < rows; ++i) {
        std::vector <int> one_row;
        for (int j = 0; j < cols; ++j) {
            one_row.push_back(EMPTY);
        }
        board.push_back(one_row);
    }
} 

void Tetris::loadTop10Scores() { // done
    std::ifstream fin;
    fin.open("top10Scores.txt");
    if (!fin.is_open()) {
        // if the file does not exist, then create a new file
        std::ofstream fout;
        fout.open("top10Scores.txt");
        for (int i = 0; i < 10; ++i) {
            fout << 0 << std::endl;
        }
    } else {
        // if the file exists, then load the top 10 scores
        for (int i = 0; i < 10; ++i) {
            fin >> top10Scores[i];
        }
    }
    fin.close();
}

void Tetris::createBlock() { // done
    delete curBlock;
    curBlock = nextBlock;
    nextBlock = new Block();
    // randomly move the block to the left or right
    int move = rand() % (cols - 2 + 1);
    curBlock->moveLeftRight(move);
}

void Tetris::createPreBlock() { // done
    Block tmpBlock;
    preBlock = *curBlock;
    while (!preBlock.checkCollision(board)) {
        tmpBlock = preBlock;
        preBlock.drop();
    }
    preBlock = tmpBlock;
}

void Tetris::clearLine() { // done
    // this function will check the board from the bottom to the top
    for (int i = rows-1, k = rows-1; i >= 0; --i) {
        // check if all the elements in the line are not -1
        if (std::find(board[i].begin(), board[i].end(), EMPTY) == board[i].end()) {
            // if all this line is full, then ignore this line
            eliminatedLines += 1;
            combo += 1;
            updateScoreLevelFlag = true;
            continue;
        }
        board[k--] = board[i];
    }
}

void Tetris::updateScore() { // done
    // the score update is based on the combo 
    // Rule: 1 combo ~ 2 combo 100 Points per line
    //       3 combo ~ 4 combo 200 Points per line
    //       5 combo ~ more 400 Points per line
    if (combo >= 1 && combo <= 2) { 
        score += 100 * combo;
    } else if (combo >= 3 && combo <= 4) {
        score += 200 * combo;
    } else if (combo >= 5) {
        score += 400 * combo;
    }
    combo = 0;
}

void Tetris::updateLevel() { // done
    // the level update is based on the score
    if (score < levelScore[0]) {
        curLevel = EASY;
    } else if (score < levelScore[1]) {
        curLevel = NORMAL;
    } else if (score < levelScore[2]) {
        curLevel = HARD;
    } else if (score < levelScore[3]) {
        curLevel = EXPERT;
    } else if (score < levelScore[4]) {
        curLevel = HELL;
    } else {
        gameOver = true;
    }
}

void Tetris::updateTimer() { // done
    // update the current time and the game time
    for (; gameStart; delay_fps(60)) {
        curTime = clock();
        gameTime = (curTime - startTime) / 1000;
    }
}

void Tetris::delay_fps(int fps) { // done
    // convert fps to delay
    std::this_thread::sleep_for(std::chrono::milliseconds(1000 / fps)); // delay 1/fps seconds, 1000ms = 1s, 1s/fps = 1/fps seconds
}

void Tetris::keyEvent() { // done
    // Direction key
    // up: u_char key = 224; key = 72;
    //     stand for rotate the block
    // down: u_char key = 224; key = 80;
    //       stand for speed up the block to the bottom (curSpeed / 2)
    // left: u_char key = 224; key = 75;
    //       stand for move the block to the left
    // right: u_char key = 224; key = 77;
    //        stand for move the block to the right

    // additional rules:
    // 'w' is the same as 'up', 'a' is the same as 'left', 'd' is the same as 'right', 's' is the same as 'down'
    // if 'space' is pressed, the block will be moved to the bottom
    // if 'p' is pressed, the game will be paused or resumed 
    // if 'q' is pressed, the game will be over

    unsigned char key = '\0';
    bool rotateFlag = false;
    bool speedUpFlag = false;
    bool droopFlag = false;
    int dx = 0;

    clock_t pressTime = clock();
	if (_kbhit()) {
		key = _getch();
        pressTime = clock();
		if (key == 224) {
			key = _getch();
			switch (key) {
			case 72: rotateFlag = true;  break;
			case 80: speedUpFlag = true; break;
			case 75: dx = -1; break;
			case 77: dx = 1;  break;
			default: break;
			}
		}
		else {
			switch (key) {
			case 'w': case 'W': rotateFlag = true;  break;
			case 's': case 'S': speedUpFlag = true; break;
			case 'a': case 'A': dx = -1; break;
			case 'd': case 'D': dx = 1;  break;
			case 'p': case 'P': gamePause = !gamePause; break;
			case ' ': droopFlag = true; break;
            case 'q': case 'Q': gameOver = true; break;
			default: break;
			}
		}
	}

    if (gamePause || gameOver ) {
        return;
    }

	if (rotateFlag) {
		rotate();
		rotateFlag = false;
	}

	if (speedUpFlag) {
        drop();
		speedUpFlag = false;
	}

	if (droopFlag) {
        droop();
		droopFlag = false;
	}

	if (dx != 0) {
		moveLeftRight(dx);
		dx = 0;
	}
}

void Tetris::drop() { // done
    bakBlock = *curBlock;
    curBlock->drop();
    if (checkCollision()) {
        bakBlock.solidify(board);
        clearLine();
        createBlock();
    }
    checkGameOver();
    updateWindowFlag = true;
}

void Tetris::droop() { // done
    while (!lock_createPreBlock) {/* blank */} // blank run, wait for the complete of preBlock
    Block* oldBlock = curBlock;
    Block* droopBlock = new Block();
    *droopBlock = preBlock;
    curBlock = droopBlock;
    delete oldBlock;
}

void Tetris::moveLeftRight(int direction) { // done
    bakBlock = *curBlock;
    curBlock->moveLeftRight(direction);
    if (checkCollision()) {
        *curBlock = bakBlock;
    }
    updateWindowFlag = true;
}

void Tetris::rotate() { // done
    if (curBlock->getType() == 6) {
        return;
    }
    bakBlock = *curBlock;
    curBlock->rotate();
    if (checkCollision()) {
        *curBlock = bakBlock;
    }
    updateWindowFlag = true;
}

bool Tetris::checkCollision() { // done
    return curBlock->checkCollision(board);
}

void Tetris::checkGameOver() { // done
    // if the new block is not valid, then the game is over
    gameOver = curBlock->checkCollision(board);
}

void Tetris::updateTop10ScoresFile() { // done
    // compare the score with the top 10 scores
    // if the score is in the top 10, then update the top 10 scores file
    for (int i = 0; i < 10; ++i) {
        if (score > top10Scores[i]) {
            // put the score in this position
            top10Scores.insert(top10Scores.begin() + i, score);
            top10Scores.pop_back();
            break;
        }
    }
    // update the top 10 scores file
    std::ofstream fout;
    fout.open("top10scores.txt");
    for (int i = 0; i < 10; ++i) {
        fout << top10Scores[i] << std::endl;
    }
    fout.close();
}

void Tetris::updateHistoryFile() { // done
    std::ofstream fout;
    fout.open("history.txt", std::ios::app);
    // [starttime] [gametime] [score]
    fout << "[StartTime: " << startTime << "] [GameTime: " << gameTime << "] [Score: " << score << "]" << std::endl;
    fout.close();
}

void Tetris::checkPause() { // done
    while (gamePause) {
        // blank run, wait for the game to be resumed
    }
}