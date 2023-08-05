#include <iostream>

const int MaxLen = 10;

using namespace std;

int main() {

    // m is the length of the queue, and n the number of commands
    int m, n;
    cin >> m >> n;
    cin.get();

    char queue[MaxLen] = {'\0'};
    int front = 0, rear = 0;

    char command[4] = {'\0'};

    while (n--) {
        cin.getline(command, 4);
        if (command[0] == '1') {
            rear = (rear+1) % m;
            queue[rear] = command[2];
        } else {
            front = (front+1) % m;
        }
        cout << front << " " << rear << endl;
    }

    while (front != rear) {
        front = (front+1) % m;
        cout << queue[front];
    }

    return 0;
}