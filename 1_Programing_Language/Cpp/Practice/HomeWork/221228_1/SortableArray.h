#include <iostream>

template <typename T>
class SortableArray {

public:

    SortableArray(int size);
    ~SortableArray();

    void pushBack(T value);
    void sort();
    void printArray();

private:

    void expand();
    int partition(int low, int high);
    void swap(T &a, T &b);
    void quickSort(int low, int high);

private:

    T* arr;
    int size;
    int count;

};

template <typename T>
SortableArray<T>::SortableArray(int size)
{
    this->size = size;
    this->count = 0;
    this->arr = new T[size];
}

template <typename T>
SortableArray<T>::~SortableArray()
{
    delete[] this->arr;
}


template <typename T>
void SortableArray<T>::expand() {
    this->size *= 2;
    T *temp = new T[this->size];
    for (int i = 0; i < this->count; ++i) {
        temp[i] = this->arr[i];
    }
    delete[] this->arr;
    this->arr = temp;
}

template <typename T>
int SortableArray<T>::partition(int low, int high) {
    T pivot = this->arr[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (this->arr[j] < pivot) {
            i += 1;
            this->swap(this->arr[i], this->arr[j]);
        }
    }
    this->swap(this->arr[i + 1], this->arr[high]);
    return i + 1;
}

template <typename T>
void SortableArray<T>::swap(T &a, T &b) {
    T temp = a;
    a = b;
    b = temp;
}

template <typename T>
void SortableArray<T>::quickSort(int low, int high) {
    if (low < high) {
        int pi = this->partition(low, high);
        this->quickSort(low, pi - 1);
        this->quickSort(pi + 1, high);
    }
}

template <typename T>
void SortableArray<T>::pushBack(T value) {
    if (this->count == this->size) {
        this->expand();
    }
    this->arr[this->count] = value;
    count += 1;
}

template <typename T>
void SortableArray<T>::sort() {
    // quick sort
    int low = 0;
    int high = this->count - 1;
    this->quickSort(low, high);
}

template <typename T>
void SortableArray<T>::printArray() {
    for (int i = 0; i < this->count; ++i) {
        std::cout << this->arr[i];
        if (i != this->count - 1) {
            std::cout << " ";
        } 
    }
    std::cout << std::endl;
}