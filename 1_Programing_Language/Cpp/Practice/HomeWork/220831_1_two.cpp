#include<iostream>
#define LEN 16

using namespace std;

// change the number into bin
int * Bin(int num) {
    int * bin = new int[LEN];
    for(int i = LEN-1; i >= 0; --i) {
        bin[i] = num % 2;
        num /= 2;
    }
    return bin;
}
// move the bin
int * Move(int *bin, int n) {
    int * newBin = new int[LEN];
    for(int i = 0; i < LEN; ++i) {
        newBin[i] = bin[(i+n+16)%16];
    }
    delete bin;
    return newBin;
}
// show
void show(int *arr) {
    for(int i = 0; i < LEN; ++i) {
        cout << arr[i];
        if (i == 7) {
            cout << " ";
        }
    }
    cout << endl;
}

int main() {
    int num, n;
    cin >> num >> n;

    int *bin = Bin(num);
    show(bin);

    bin = Move(bin, n);
    show(bin);

    delete bin;

    return 0;
}