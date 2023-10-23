#include <stdio.h>
#include <string.h>

char board[3][3];

void init_board() {
    for (int i = 0; i < 3; ++i) {
        memset(board[i], ' ', 3);
    }
}

int check_result(char player1, char player2) {
    // check win
    int row_sum[3] = {0}, col_sum[3] = {0}, diag_sum[3] = {0};
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j <3; ++j) {
            row_sum[i] += board[i][j];
            col_sum[j] += board[i][j];
        }
        diag_sum[0] += board[i][i];
        diag_sum[1] += board[i][2-i];
    }

    for (int i = 0; i < 3; ++i) {
        if (row_sum[i] == player1 * 3 || col_sum[i] == player1 * 3 || diag_sum[i] == player1 * 3) {
            return 1;
        } else if (row_sum[i] == player2 * 3 || col_sum[i] == player2 * 3 || diag_sum[i] == player2 * 3) {
            return 2;
        }
    }

    return 3;
}


void print_result(int res) {
    switch (res) {
    case 1:
        printf("player1 won"); break;
    case 2:
        printf("player2 won"); break;
    case 3:
        printf("draw"); break;
    case 4:
        printf("unfinished"); break;
    default:
        break;
    }
    printf("\n");
}


int main() {

    int N; scanf("%d", &N);

    for (int i = 0; i < N; ++i) {
        printf("test case %d:\n", i + 1);
        init_board();
        int n; scanf("%d", &n);
        int flag = 0;
        for (int j = 0; j < n; ++j) {
            int x, y; char c;
            scanf("%d %d %c", &x, &y, &c);
            board[x-1][y-1] = c;
            if (flag != 1 && flag != 2) {
                flag = check_result('X', 'O'); 
            }
            print_result(flag == 3 && j != n-1 ? 4 : flag);
        }
    }

    return 0;
}