// 循环移位

#include<iostream>
#define CARRY 2
#define N 100

inline int MAX(int x, int y) {return (x > y ? x : y);}

using namespace std;

typedef struct Data {
    int *bin;
    int cont;
}Data;


// move the numebr
void Move(Data data, int n) {
    int bin[16] = {0};
    int cont = data.cont;

    for(int i = 0; i < cont + 1; ++i) {
        bin[i+15-cont] = data.bin[cont-i];
    }

    int newBin[16] = {0};
    for(int i = 0; i < 16; ++i) {
        newBin[i] = bin[(i+n+16)%16];
    }

    for(int i = 0; i < 16; ++i) {
        cout << bin[i];
        if ((i+1) % 8 == 0 && i != 15) {
            cout << " ";
        }
    }
    cout << endl;
    
    for(int i = 0; i < 16; ++i) {
        cout << newBin[i];
        if ((i+1) % 8 == 0 && i != 15) {
            cout << " ";
        }
    }
}


// change the number into bin
Data Binary(int num) {
    Data data;
    int bin[N] = {0};
    int cont = 0;
    int ord;
    while(num) {
        ord = 0;
        bin[0] ++;
        num --;
        while(bin[ord] == CARRY) {
            bin[ord] = 0;
            bin[++ord] ++;
            cont = MAX(cont, ord);
        }
    }
    data.bin = bin;
    data.cont = cont;
    return data;
}

int main() {
    int num, n;
    cin >> num >> n;
    Data data = Binary(num);
    Move(data, n);
    return 0;
}