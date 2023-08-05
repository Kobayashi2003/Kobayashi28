#include <iostream>

using namespace std;

template <typename T>
void print(T **arr, int n, int m) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            cout << arr[i][j] << "\t";
        }
        cout << endl;
    }
    cout << endl;
}

int main() {

    int n, m; cin >> n >> m; cin.ignore();
    char **logo = new char*[n];

    for (int i = 0; i < n; ++i)
        logo[i] = new char[m];

    int **count = new int*[n+1];
    for (int i = 0; i < n+1; ++i)
        count[i] = new int[m+1];
    for (int i = 0; i < n+1; ++i) 
        count[i][m] = 1;
    for (int i = 0; i < m+1; ++i)
        count[n][i] = 1;

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            char ch; cin.get(ch);
            if (ch == '\r' || ch == '\n') {
                cin.get(ch);
            }
            logo[i][j] = ch;
            if (i == 0 || j == 0 || logo[i][j] != logo[i-1][j] || logo[i][j] != logo[i][j-1] || logo[i][j] != logo[i-1][j-1]) {
                count[i][j] = 1;
            } else {
                // count[i][j] = count[i-1][j] + count[i][j-1] + count[i-1][j-1];
                count[i][j] = 0;
            }
        }
    }

    print(logo, n, m);
    print(count, n, m);

    char **log_compressed = new char*[n];
    for (int i = 0; i < n; ++i) {
        log_compressed[i] = new char[m];
    }
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (count[i][j] == 1 && count[i+1][j] == 1 && count[i][j+1] == 1) {
                log_compressed[i][j] = logo[i][j];
            } else {
                log_compressed[i][j] = ' ';
            }
        }
    }

    print(log_compressed, n, m);

    return 0;
}