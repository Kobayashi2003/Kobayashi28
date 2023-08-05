#include <iostream>
#include <string>

using namespace std;

const int MAX_NUM = 1024;
const int MAX_LEN = 1024;

int main() {
    string strs[MAX_NUM];
    
    int N;
    cin >> N;
    cin.get();
    for (int i = 0; i < N; ++i) {
        getline(cin, strs[i]);
    }

    int cont = 0;
    while (cont < N) {
        cont = 0;

        // find the shortest string in the strs
        int min_len = MAX_LEN;
        int min;
        for (int i = 0; i < N; ++i) {
            if (strs[i] != "" && (const int)strs[i].length() < min_len) {
                min = i;
                min_len = strs[i].length();
            }
        }
        cout << strs[min] << endl;
        strs[min] = "";

        for (int i = 0; i < N; ++i) {
            if (strs[i] == "") {
                cont += 1;
            }
        }
    }

    return 0;
}
