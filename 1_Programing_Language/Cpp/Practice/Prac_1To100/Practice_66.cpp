#include <iostream>
#include <initializer_list>

template <typename T>
using initList = std::initializer_list<T>; 

class Matrix {
private:
    int _row;
    int _col;
    int **_data;
public:
    Matrix() : _row(0), _col(0), _data(nullptr) {}
    // init list {...}
    Matrix (initList<double> list) {
        _row = 1;
        _col = list.size();
        _data = new int*[_row]{ nullptr };
        _data[0] = new int[_col]{ 0 };
        for (int i = 0; i < _col; i++) {
            _data[0][i] = list.begin()[i];
        }
    }
    // init list {{}, {}, ...}
    Matrix (initList< initList<double> > list) {
        _row = list.size();
        _col = list.begin()->size();
        _data = new int*[_row]{ nullptr };
        for (int i = 0; i < _row; ++i) {
            _data[i] = new int[_col]{ 0 };
            for (int j = 0; j < _col; ++j) {
                _data[i][j] = list.begin()[i].begin()[j];
            }
        }
    }
    // copy constructor with left value
    Matrix (const Matrix& m) {
        _row = m._row;
        _col = m._col;
        _data = new int*[_row]{ nullptr };
        for (int i = 0; i < _row; ++i) {
            _data[i] = new int[_col]{ 0 };
            for (int j = 0; j < _col; ++j) {
                _data[i][j] = m._data[i][j];
            }
        }
    }
    // copy constructor with right value
    Matrix (Matrix&& m) {
        _row = m._row;
        _col = m._col;
        _data = m._data;
        m._data = nullptr;
    }
   // destructor
    ~Matrix() {
        if (_data != nullptr) {
            for (int i = 0; i < _row; ++i) {
                delete[] _data[i];
            }
            delete[] _data;
        }
    }
    // Matrix + Matrix
    Matrix operator+ (const Matrix& m) {
        Matrix result;
        if (_row == m._row && _col == m._col) {
            result._row = _row;
            result._col = _col;
            result._data = new int*[result._row]{ nullptr };
            for (int i = 0; i < result._row; ++i) {
                result._data[i] = new int[result._col]{ 0 };
                for (int j = 0; j < result._col; ++j) {
                    result._data[i][j] = _data[i][j] + m._data[i][j];
                }
            }
        }
        return result;
    }
    // Matrix - Matrix
    Matrix operator- (const Matrix& m) {
        Matrix result;
        if (_row == m._row && _col == m._col) {
            result._row = _row;
            result._col = _col;
            result._data = new int*[result._row]{ nullptr };
            for (int i = 0; i < result._row; ++i) {
                result._data[i] = new int[result._col]{ 0 };
                for (int j = 0; j < result._col; ++j) {
                    result._data[i][j] = _data[i][j] - m._data[i][j];
                }
            }
        }
        return result;
    }
    // Matrix * Matrix
    Matrix operator* (const Matrix& m) {
        Matrix result;
        if (_col == m._row) {
            result._row = _row;
            result._col = m._col;
            result._data = new int*[result._row]{ nullptr };
            for (int i = 0; i < result._row; ++i) {
                result._data[i] = new int[result._col]{ 0 };
                for (int j = 0; j < result._col; ++j) {
                    for (int k = 0; k < _col; ++k) {
                        result._data[i][j] += _data[i][k] * m._data[k][j];
                    }
                }
            }
        }
    }
    // Matrix * int
    Matrix operator* (const int& n) {
        Matrix result;
        result._row = _row;
        result._col = _col;
        result._data = new int*[result._row]{ nullptr };
        for (int i = 0; i < result._row; ++i) {
            result._data[i] = new int[result._col]{ 0 };
            for (int j = 0; j < result._col; ++j) {
                result._data[i][j] = _data[i][j] * n;
            }
        }
        return result;
    }
    // int * Matrix
    friend Matrix operator* (const int& n, const Matrix& m) {
        Matrix result;
        result._row = m._row;
        result._col = m._col;
        result._data = new int*[result._row]{ nullptr };
        for (int i = 0; i < result._row; ++i) {
            result._data[i] = new int[result._col]{ 0 };
            for (int j = 0; j < result._col; ++j) {
                result._data[i][j] = m._data[i][j] * n;
            }
        }
        return result;
    }
    // Matrix / int
    Matrix operator/ (const int& n) {
        Matrix result;
        result._row = _row;
        result._col = _col;
        result._data = new int*[result._row]{ nullptr };
        for (int i = 0; i < result._row; ++i) {
            result._data[i] = new int[result._col]{ 0 };
            for (int j = 0; j < result._col; ++j) {
                result._data[i][j] = _data[i][j] / n;
            }
        }
        return result;
    }
    // Matrix += Matrix
    Matrix& operator+= (const Matrix& m) {
        if (_row == m._row && _col == m._col) {
            for (int i = 0; i < _row; ++i) {
                for (int j = 0; j < _col; ++j) {
                    _data[i][j] += m._data[i][j];
                }
            }
        }
        return *this;
    }
    // Matrix -= Matrix
    Matrix& operator-= (const Matrix& m) {
        if (_row == m._row && _col == m._col) {
            for (int i = 0; i < _row; ++i) {
                for (int j = 0; j < _col; ++j) {
                    _data[i][j] -= m._data[i][j];
                }
            }
        }
        return *this;
    }
    // Matrix *= Matrix
    Matrix& operator*= (const Matrix& m) {
        if (_col == m._row) {
            Matrix result;
            result._row = _row;
            result._col = m._col;
            result._data = new int*[result._row]{ nullptr };
            for (int i = 0; i < result._row; ++i) {
                result._data[i] = new int[result._col]{ 0 };
                for (int j = 0; j < result._col; ++j) {
                    for (int k = 0; k < _col; ++k) {
                        result._data[i][j] += _data[i][k] * m._data[k][j];
                    }
                }
            }
            *this = result;
        }
        return *this;
    }
    // Matrix *= int
    Matrix& operator*= (const int& n) {
        for (int i = 0; i < _row; ++i) {
            for (int j = 0; j < _col; ++j) {
                _data[i][j] *= n;
            }
        }
        return *this;
    }
    // Matrix /= int
    Matrix& operator/= (const int& n) {
        for (int i = 0; i < _row; ++i) {
            for (int j = 0; j < _col; ++j) {
                _data[i][j] /= n;
            }
        }
        return *this;
    }
    // Matrix == Matrix
    bool operator== (const Matrix& m) {
        if (_row == m._row && _col == m._col) {
            for (int i = 0; i < _row; ++i) {
                for (int j = 0; j < _col; ++j) {
                    if (_data[i][j] != m._data[i][j]) {
                        return false;
                    }
                }
            }
            return true;
        }
        return false;
    }
    // Matrix != Matrix
    bool operator!= (const Matrix& m) {
        if (_row == m._row && _col == m._col) {
            for (int i = 0; i < _row; ++i) {
                for (int j = 0; j < _col; ++j) {
                    if (_data[i][j] != m._data[i][j]) {
                        return true;
                    }
                }
            }
            return false;
        }
        return true;
    }
    // Matrix = int
    Matrix& operator= (const int& n) {
        for (int i = 0; i < _row; ++i) {
            for (int j = 0; j < _col; ++j) {
                _data[i][j] = n;
            }
        }
        return *this;
    }
    // Matrix = Matrix
     // copy assignment with left value
    Matrix& operator= (const Matrix& m) {
        if (this != &m) {
            _row = m._row;
            _col = m._col;
            _data = new int*[_row]{ nullptr };
            for (int i = 0; i < _row; ++i) {
                _data[i] = new int[_col]{ 0 };
                for (int j = 0; j < _col; ++j) {
                    _data[i][j] = m._data[i][j];
                }
            }
        }
        return *this;
    }
    // copy assignment with right value
    Matrix& operator= (Matrix&& m) {
        if (this != &m) {
            _row = m._row;
            _col = m._col;
            _data = m._data;
            m._data = nullptr;
        }
        return *this;
    }
    // Matrix = initializer_list
    Matrix& operator= (const std::initializer_list<std::initializer_list<int>>& list) {
        _row = list.size();
        _col = list.begin()->size();
        _data = new int*[_row]{ nullptr };
        int i = 0;
        for (auto& row : list) {
            _data[i] = new int[_col]{ 0 };
            int j = 0;
            for (auto& col : row) {
                _data[i][j] = col;
                ++j;
            }
            ++i;
        }
        return *this;
    }

    // print
    void print() {
        for (int i = 0; i < _row; ++i) {
            for (int j = 0; j < _col; ++j) {
                std::cout << _data[i][j] << " ";
            }
            std::cout << std::endl;
        }
    }
    // overload operator<<
    friend std::ostream& operator<< (std::ostream& os, const Matrix& m) {
        for (int i = 0; i < m._row; ++i) {
            for (int j = 0; j < m._col; ++j) {
                os << m._data[i][j] << " ";
            }
            os << std::endl;
        }
        return os;
    }
    // overload operator>>
    friend std::istream& operator>> (std::istream& is, Matrix& m) {
        std::cout << "Enter row: ";
        is >> m._row;
        std::cout << "Enter col: ";
        is >> m._col;
        m._data = new int*[m._row]{ nullptr };
        for (int i = 0; i < m._row; ++i) {
            m._data[i] = new int[m._col]{ 0 };
            for (int j = 0; j < m._col; ++j) {
                std::cout << "Enter data[" << i << "][" << j << "]: ";
                is >> m._data[i][j];
            }
        }
        return is;
    }
};

int main() {
    // test the program
    
    return 0;
}