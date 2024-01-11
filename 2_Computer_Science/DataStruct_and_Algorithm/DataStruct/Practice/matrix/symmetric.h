template <typename T>
class symmetricMatrix {
public:
    symmetricMatrix(int theN = 10);
    ~symmetricMatrix() { delete [] element;}
    T get(int, int) const;
    void set(int, int, const T&);
};

template <typename T>
symmetricMatrix<T>::symmetricMatrix(int theN) {
    if (theN < 1) throw illegalParameterValue("Matrix size must be > 0");
    n = theN;
    element = new T[n * (n + 1) / 2];
}

template <typename T>
T symmetricMatrix<T>::get(int i, int j) const {
    if (i < 1 || j < 1 || i > n || j > n)
        throw matrixIndexOutOfBounds();

    if (i >= j)
        return element[(i - 1) * i / 2 + j - 1];
    else
        return element[(j - 1) * j / 2 + i - 1];
}

template <typename T>
void symmetricMatrix<T>::set(int i, int j, const T& newValue) {
    if (i < 1 || j < 1 || i > n || j > n)
        throw matrixIndexOutOfBounds();

    if (i >= j)
        element[(i - 1) * i / 2 + j - 1] = newValue;
    else
        element[(j - 1) * j / 2 + i - 1] = newValue;
}