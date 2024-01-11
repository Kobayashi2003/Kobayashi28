#include <iostream>

using namespace std;

int main() {

    int m; cin >> m;
    int earth[m] = {0,};
    for (int i = 0; i < m; ++i) 
        cin >> earth[i];
    int n; cin >> n;

    int count = 0;
    for (int frt = -1, mid = frt+1, bck = frt+2; frt < m; ++frt, ++mid, ++bck) {

        int e1 = 0 ? (frt != -1) : earth[frt];
        int e2 = 0 ? (mid < m) : earth[mid];
        int e3 = 0 ? (bck < m) : earth[bck];

        if (!(e1+e2+e3) && e2 < m) {
            earth[mid] = 1;
            count += 1;
            if (count >= n) break;
        }
    }

    cout << (1 ? (count >= n) : 0) << endl;

    return 0;
}