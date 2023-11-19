#include <iostream>
#include <vector>

using namespace std;


int main() {

    int n; cin >> n;

    vector<int> weight(n);
    for (int i = 0; i < n; i++) {
        cin >> weight[i];
    }

    vector<int> haffman(2*n-1);
    vector<int> parent(2*n-1, -1);
    for (int i = 0; i < n; i++) {
        haffman[i] = weight[i];
    }

    for (int i = n; i < 2*n-1; ++i) {
        int min1 = 1e9, min2 = 1e9;
        int min1_index = -1, min2_index = -1;
        for (int j = 0; j < i; ++j) {
            if (parent[j] == -1) {
                if (haffman[j] < min1) {
                    min2 = min1;
                    min2_index = min1_index;
                    min1 = haffman[j];
                    min1_index = j;
                } else if (haffman[j] < min2) {
                    min2 = haffman[j];
                    min2_index = j;
                }
            }
        }   
        haffman[i] = min1 + min2;
        parent[min1_index] = i;
        parent[min2_index] = i;
    }

    int ans = 0;
    for (int i = 0; i < n; ++i) {
        int pth = 0;
        for (int j = i; j != -1; j = parent[j]) {
            pth++;
        }
        ans += (pth-1) * weight[i];
    }

    cout << ans << endl;
    
    return 0;
}