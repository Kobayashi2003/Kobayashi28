// 斐波那契数列

#include<iostream>

using namespace std;

int main() {
    int num;
    cin >> num;
    int n1=1, n2=1, tmp, cont=2;
    while(n2 < num) {
        tmp = n2;
        n2 += n1;
        n1 = tmp;
        cont ++;
    }
    cout << ( (n2-num) < (num-n1) ? cont : cont-1);
    return 0;
}