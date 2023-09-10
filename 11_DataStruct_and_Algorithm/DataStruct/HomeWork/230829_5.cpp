#include <iostream>

using namespace std;

int main() {

    int board[4][4] = {0,};
    for (int i = 0; i < 4; ++i) 
        for (int j = 0; j < 4 ; ++j)
            cin >> board[i][j];

    int value[4][4] = {0,};
    value[0][0] = board[0][0];
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (j+1 < 4 && value[i][j+1] < value[i][j] + board[i][j+1]) {
                value[i][j+1] = value[i][j] + board[i][j+1];
            }
            if (i+1 < 4 && value[i+1][j] < value[i][j] + board[i+1][j]) {
                value[i+1][j] = value[i][j] + board[i+1][j];
            }
        }
    }

    cout << value[3][3] << endl;

    return 0;
}