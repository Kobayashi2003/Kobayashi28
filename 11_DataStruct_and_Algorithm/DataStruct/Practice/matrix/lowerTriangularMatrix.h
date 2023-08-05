template <typename T>
class lowerTriangularMatrix {
public:
    lowerTriangularMatrix(int theN = 10);
    ~lowerTriangularMatrix() { delete [] element;}
    T get(int, int) const;
    void set(int, int, const T&);
private:
    int n;
    T *element; 
};

template <typename T>
lowerTriangularMatrix<T>::lowerTriangularMatrix(int theN) {
    if (theN < 1) throw illegalParameterValue("Matrix size must be > 0");
    n = theN;
    element = new T[n * (n + 1) / 2];
}

template <typename T>
void lowerTriangularMatrix<T>::set(int i, int j, const T& newValue) {
    if (i < 1 || j < 1 || i > n || j > n)
        throw matrixIndexOutOfBounds();
    
    if (i >= j)
        element[(i - 1) * i / 2 + j - 1] = newValue;
    else
        if (newValue != 0)
            throw illegalParameterValue("elements not in lower triangular matrix must be 0");
} 