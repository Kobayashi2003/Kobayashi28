#ifndef BINARY_HEAP_H
#define BINARY_HEAP_H
#include <vector>
#include <iostream>

using namespace std;

template <typename Comparable> 
class BinaryHeap {
public: 
    explicit BinaryHeap(int capacity = 100);
    explicit BinaryHeap(const vector<Comparable> & items); 

    bool isEmpty() const;
    const Comparable & findMin() const;

    void insert(const Comparable & x);
    void insert(Comparable && x);
    void deleteMin();
    void deleteMin(Comparable & minItem);
    void makeEmpty();

    void showHeap() const {
        int j = 1;
        for (int i = 1; i <= currentSize; ++i) {
            cout << array[i];
            if (i == j) {
                cout << endl;
                j = j * 2 + 1;
            }
            else
                cout << " ";
        }
        cout << endl;
    }

private:
    int currentSize; // Number of elements in heap 
    vector<Comparable> array; // The heap array

    void buildHeap();
    void percolateDown(int hole);
};

template <typename Comparable>
BinaryHeap<Comparable>::BinaryHeap(int capacity) : currentSize(capacity), array(capacity + 1) {}


template <typename Comparable>
BinaryHeap<Comparable>::BinaryHeap(const vector<Comparable> & items) 
    : currentSize{items.size()}, array(items.size() + 10) 
{
    for (int i = 0; i < items.size(); ++i) 
        array[i + 1] = items[i];
    buildHeap();    
}


template <typename Comparable>
void BinaryHeap<Comparable>::buildHeap() {
    for (int i = currentSize / 2; i > 0; --i)
        percolateDown(i);
}


template <typename Comparable>
bool BinaryHeap<Comparable>::isEmpty() const {
    return currentSize == 0;
}


template <typename Comparable>
const Comparable & BinaryHeap<Comparable>::findMin() const {
    if (isEmpty())
        // throw UnderflowException{};
        return array[0];
    return array[1];
}


template <typename Comparable>
void BinaryHeap<Comparable>::insert(const Comparable & x) {
    if (currentSize == array.size() - 1)
        array.resize(array.size() * 2);

    // Percolate up
    int hole = ++currentSize;
    Comparable copy = x;

    array[0] = std::move(copy);
    for (; x < array[hole / 2]; hole /= 2)
        array[hole] = std::move(array[hole / 2]);
    array[hole] = std::move(array[0]);
}


template <typename Comparable>
void BinaryHeap<Comparable>::insert(Comparable && x) {
    if (currentSize == array.size() - 1)
        array.resize(array.size() * 2);

    // Percolate up
    int hole = ++currentSize;
    for (; hole > 1 && x < array[hole / 2]; hole /= 2)
        array[hole] = std::move(array[hole / 2]);
    array[hole] = std::move(x);
}


template <typename Comparable>
void BinaryHeap<Comparable>::deleteMin() {
    if (isEmpty())
        // throw UnderflowException{};
        return;
    array[1] = std::move(array[currentSize--]);
    percolateDown(1);
}


template <typename Comparable>
void BinaryHeap<Comparable>::deleteMin(Comparable & minItem) {
    if (isEmpty())
        // throw UnderflowException{};
        return;
    minItem = std::move(array[1]);
    array[1] = std::move(array[currentSize--]);
    percolateDown(1);
}


template <typename Comparable>
void BinaryHeap<Comparable>::percolateDown(int hole) {
    int child;
    Comparable tmp = std::move(array[hole]);
    for (; hole*2 <= currentSize; hole = child) {
        child = hole * 2;
        if (child != currentSize && array[child + 1] < array[child])
            ++child;
        if (array[child] < tmp)
            array[hole] = std::move(array[child]);
        else
            break;
    }
    array[hole] = std::move(tmp);
}

 
template <typename Comparable>
void BinaryHeap<Comparable>::makeEmpty() {
    currentSize = 0;
}

#endif