#include <iostream>

class Matrix {
private:
    int (*_matrix)[3];
public:
    Matrix() : _matrix(new int [2][3]) {}
    Matrix(int (*matrix)[3]) {
        int (*data)[3] = new int[2][3];
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 3; j++) {
                data[i][j] = matrix[i][j];
            }
        }
        _matrix = data;
    }
    ~Matrix() {
        delete [] _matrix;
    }
    Matrix operator+(const Matrix& m) {
        int (*result)[3] = new int[2][3];
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 3; j++) {
                result[i][j] = _matrix[i][j] + m._matrix[i][j];
            }
        }
        return Matrix(result);
    }
    friend std::ostream& operator<<(std::ostream& os, const Matrix& m) {
        for (int i = 0; i < 2; ++i) {
            for (int j = 0; j < 3; ++j) {
                os << m._matrix[i][j] << " ";
            }
            os << std::endl;
        }
        return os;
    }
    friend std::istream& operator>>(std::istream& is, Matrix& m) {
        for (int i = 0; i < 2; ++i) {
            for (int j = 0; j < 3; ++j) {
                is >> m._matrix[i][j];
            }
        }
        return is;
    }
};

int main() {
    Matrix m1, m2;
    std::cin >> m1 >> m2;
    std::cout << "output the result of m1 + m2:" << std::endl;
    std::cout << m1 + m2;
    return 0;
}