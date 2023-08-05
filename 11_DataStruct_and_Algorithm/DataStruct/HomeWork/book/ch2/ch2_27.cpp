#include <iostream>

using namespace std;

int matrix[4][4] = {
    {1, 2, 8, 9},
    {2, 4, 9, 12},
    {4, 7, 10, 13},
    {6, 8, 11, 15}
};

bool find_number(int matrix[][4], int N, int target) {
    int row = 0, col = N -1;
    while (matrix[row][col] != target) {
        if (matrix[row][col] > target) {
            col--;
        } else {
            row++;
        }
        if (row >= N || col < 0) {
            return false;
        }
    }
    return true;
}


int main() {

    int target = 7;
    bool result = find_number(matrix, 4, target);
    cout << "result: " << result << endl;
    return 0;

}