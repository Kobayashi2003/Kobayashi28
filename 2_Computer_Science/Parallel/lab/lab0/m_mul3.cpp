#include <iostream>
#include <vector>
#include <chrono>
#include <random>

using namespace std;

void matrix_multiply(const vector<vector<double>>& A, const vector<vector<double>>& B, vector<vector<double>>& C) {
    int rows_a = A.size();
    int cols_a = A[0].size();
    int rows_b = B[0].size();
    int cols_b = B.size();

    if (cols_a != rows_b) {
        throw invalid_argument("Invalid matrix dimensions");
    }

    C.resize(rows_a, vector<double>(cols_b, 0.0));

    auto start_time = chrono::high_resolution_clock::now();
    for (int i = 0; i < rows_a; ++i) {
        for (int j = 0; j < cols_b; ++j) {
            for (int k = 0; k < cols_a; ++k) {
                C[i][j] += A[i][k] * B[j][k];
            }
        }
    }
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time);
    cout << "Time taken to multiply two matrices: " << duration.count() << " milliseconds." << endl;
}

int main() {
    int m = 2000;
    int k = 200;
    int n = 1000;
    vector<vector<double>> A(m, vector<double>(k));
    vector<vector<double>> B(n, vector<double>(k));
    vector<vector<double>> C(m, vector<double>(n));
    
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<double> dis(0.0, 100.0);

    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < k; ++j) {
            A[i][j] = dis(gen);
        }
    }

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < k; ++j) {
            B[i][j] = dis(gen);
        }
    }

    matrix_multiply(A, B, C);

    return 0;
}
