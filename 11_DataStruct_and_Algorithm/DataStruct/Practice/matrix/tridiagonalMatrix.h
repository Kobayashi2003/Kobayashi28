#include "myExceptions.h"

template <typename T>
class tridiagonalMatrix {
public:
    tridiagonalMatrix(int theN = 10);
    ~tridiagonalMatrix() { delete [] element;}
    T get(int, int) const;
    void set(int, int, const T&);
private:
    int n;
    T *element; 
};


template <typename T>
tridiagonalMatrix<T>::tridiagonalMatrix(int theN) {
    if (theN < 1) throw illegalParameterValue("Matrix size must be > 0");
    n = theN;
    element = new T[3 * n - 2];
}

template <typename T>
T tridiagonalMatrix<T>::get(int i, int j) const {
    if (i < 1 || j < 1 || i > n || j > n)
        throw matrixIndexOutOfBounds();

    switch (i - j) {
        case -1: return element[i - 2]; // below the main diagonal
        case 0: return element[n + i - 1]; // on the main diagonal
        case 1: return element[2 * n + i - 2]; // above the main diagonal
    }
}