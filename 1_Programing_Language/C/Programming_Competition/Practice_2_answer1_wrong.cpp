#include <iostream>
#include <limits>

using namespace std;

const int MAX = 1e2;

const int OFF = 0;
const int ON = 1;

int sum = 0;

void Switch(int *state) {
    if (*state == ON) {
        *state = OFF;;
        sum -= 1;
    } else {
        *state = ON;
        sum += 1;
    }
}


void command_R(int lights[][MAX], int N, int x) {
    // switch row x
    for (int i = 0; i < N; i++) {
        Switch(&lights[i][x]);
    }
}


void command_C(int lights[][MAX], int N, int x) {
    // switch column x
    for (int i = 0; i < N; i++) {
        Switch(&lights[x][i]);
    }
}


void command_D(int lights[][MAX], int N) {
    // switch the main diagonal
    for (int i = 0; i < N; i++) {
        Switch(&lights[i][i]);
    }
}


int main() {

    int lights[MAX][MAX] = {0};

    int T;
    cin >> T;
    for (int i = 0; i < T; i++) {
        int N, M;
        cin >> N >> M;
        for (int i = 0; i < M; i++) {
            char command;
            cin.ignore(std::numeric_limits<streamsize>::max(), '\n');
            cin >> command;
            if (command == 'R') {
                int x;
                cin >> x;
                command_R(lights, N, x);
                cout << sum << endl;
            } else if (command == 'C') {
                int x;
                cin >> x;
                command_C(lights, N, x);
                cout << sum << endl;
            } else {
                command_D(lights, N);
                cout << sum << endl;
            }
        }
    }

    return 0;
}