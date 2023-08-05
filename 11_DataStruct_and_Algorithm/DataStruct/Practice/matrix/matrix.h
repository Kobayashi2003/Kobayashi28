#include "myExceptions.h"
#include <iostream> 
#include <algorithm>
#include <initializer_list>
#include <iterator>

using namespace std;

template <typename T>
class matrix {
    friend ostream& operator<<(ostream& os, const matrix<T>& m) {
        for (int i = 1; i <= m.theRows; i++) {
            for (int j = 1; j <= m.theColumns; j++) {
                os << m(i, j) << " ";
            }
            os << endl;
        }
        return os;
    }
public:
    /// constructors and destructor ///
    matrix(int theRows = 0, int theColumns = 0);
    matrix(const matrix<T>&);
    ~matrix() { delete[] element; }
    /// get ///
    int rows() const { return theRows; }
    int columns() const { return theColumns; }
    /// overload operators ///
    T& operator() (int i, int j) const;
    matrix<T>& operator=(const matrix<T>&);
    matrix<T> operator+() const; // unary +
    matrix<T> operator+(const matrix<T>&) const;
    matrix<T> operator-() const; // unary -
    matrix<T> operator-(const matrix<T>&) const;
    matrix<T> operator*(const matrix<T>&) const;
    matrix<T>& operator+=(const T&);

    using lt = std::initializer_list<T>;
    using llt = std::initializer_list<std::initializer_list<T>>;
    matrix(int, int, lt);
    matrix(int, int, llt);

private:
    int theRows, theColumns;
    T *element;
};


/// constructor ///
template <typename T>
matrix<T>::matrix(int theRows, int theColumns) {
    if (theRows < 0 || theColumns < 0) {
        throw illegalParameterValue("Rows and columns must be >= 0");
    }
    if ((theRows == 0 || theColumns == 0) && (theRows != 0 || theColumns != 0)) {
        throw illegalParameterValue("Either both or neither rows and columns should be zero");
    }

    this->theRows = theRows;
    this->theColumns = theColumns;
    element = new T[theRows * theColumns];
}

/// copy constructor ///
template <typename T>
matrix<T>::matrix(const matrix<T>& m) {
    theRows = m.theRows;
    theColumns = m.theColumns;
    element = new T[theRows * theColumns];

    copy(m.element, m.element + theRows * theColumns, element);    
}

/// overload = ///
template <typename T>
matrix<T>& matrix<T>::operator=(const matrix<T>& m) {
    if (this != &m) {
        delete [] element;
        theRows = m.theRows;
        theColumns = m.theColumns;
        element = new T[theRows * theColumns];
        copy(m.element, m.element + theRows * theColumns, element);
    }
    return *this;
}

/// overlode (i,j) ///
template <typename T>
T& matrix<T>::operator()(int i, int j) const {
    // return reference to (i,j)th element of matrix
    if (i < 1 || i > theRows || j < 1 || j > theColumns) {
        throw matrixIndexOutOfBounds();
    }
    return element[(i - 1) * theColumns + j - 1];
}

/// overload unary + ///
template <typename T>
matrix<T> matrix<T>::operator+() const {
    // return a copy of *this
    return *this;
}

/// overload + ///
template <typename T>
matrix<T> matrix<T>::operator+(const matrix<T>& m) const {
    // return the matrix w = (*this) + m
    if (theRows != m.theRows || theColumns != m.theColumns) {
        throw matrixSizeMismatch();
    }
    
    matrix<T> w(theRows, theColumns);
    for (int i = 0; i < theRows * theColumns; i++) {
        w.element[i] = element[i] + m.element[i];
    } 

    return w;
}

/// overload unary - ///
template <typename T>
matrix<T> matrix<T>::operator-() const {
    // return the matrix w = -(*this)
    matrix w(theRows, theColumns);
    for (int i = 0; i < theRows * theColumns; i++) {
        w.element[i] = -element[i];
    }

    return w;
}

/// overload - ///
template <typename T>
matrix<T> matrix<T>::operator-(const matrix<T>& m) const {
    // return the matrix w = (*this) - m
    if (theRows != m.theRows || theColumns != m.theColumns) {
        throw matrixSizeMismatch();
    }

    matrix<T> w(theRows, theColumns);
    for (int i = 0; i < theRows * theColumns; i++) {
        w.element[i] = element[i] - m.element[i];
    }

    return w;
}

/// overload * ///
template <typename T>
matrix<T> matrix<T>::operator*(const matrix<T>& m) const {
    // return the matrix w = (*this) * m
    if (theColumns != m.theRows) {
        throw matrixSizeMismatch();
    }

    matrix<T> w(theRows, m.theColumns);

    int ct = 0, cm = 0, cw = 0;

    for (int i = 1; i <= theRows; i++) {
        for (int j = 1; j <= m.theColumns; j++) {
            T sum = element[ct] * m.element[cm];
            for (int k = 2; k <= theColumns; k++) {
                ct++;
                cm += m.theColumns;
                sum += element[ct] * m.element[cm];
            }
            w.element[cw++] = sum;

            ct -= theColumns - 1;
            cm = j;
        }
        ct += theColumns;
        cm = 0;
    }

    return w;
}

/// overload += ///
template <typename T>
matrix<T>& matrix<T>::operator+=(const T& x) {
    // add x to each element of *this
    for (int i = 0; i < theRows * theColumns; i++) {
        element[i] += x;
    }

    return *this;
}


/// constructor ///
template <typename T>
matrix<T>::matrix(int theRows, int theColumns, lt list) {
    if (theRows < 0 || theColumns < 0) {
        throw illegalParameterValue("Rows and columns must be >= 0");
    }
    if ((theRows == 0 || theColumns == 0) && (theRows != 0 || theColumns != 0)) {
        throw illegalParameterValue("Either both or neither rows and columns should be zero");
    }

    this->theRows = theRows;
    this->theColumns = theColumns;
    element = new T[theRows * theColumns];

    copy(list.begin(), list.end(), element);
}

template <typename T>
matrix<T>::matrix(int theRows, int theColumns, llt list) {
    if (theRows < 0 || theColumns < 0) {
        throw illegalParameterValue("Rows and columns must be >= 0");
    }
    if ((theRows == 0 || theColumns == 0) && (theRows != 0 || theColumns != 0)) {
        throw illegalParameterValue("Either both or neither rows and columns should be zero");
    }

    this->theRows = theRows;
    this->theColumns = theColumns;
    element = new T[theRows * theColumns];

    int ct = 0;
    for (auto i = list.begin(); i != list.end(); i++) {
        copy(i->begin(), i->end(), element + ct);
        ct += theColumns;
    }
}