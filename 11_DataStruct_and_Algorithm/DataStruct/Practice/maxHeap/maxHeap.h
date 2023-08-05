template <typename T>
void maxHeap<T>::push(const T& theElement) {
    if (heapSize == arrayLength - 1) {
        changeLength1D(heap, arrayLength, 2 * arrayLength);
        arrayLength *= 2;
    }  
    int currentNode = ++heapSize;
    while (currenteNode !=1 && heap[currentNode / 2] < theElement) {
        heap[currentNode] = heap[currentNode / 2];
        currentNode /= 2;
    }
    heap[currentNode] = theElement;
} 

template <typename T>
void maxHeap<T>::pop() {
    if (heapSize == 0) 
        throw queueEmpty();
    
    heap[1].~T();

    T lastElement = heap[heapSize--];

    int currentNode = 1, child = 2;

    while (child <= heapSize) {
        if (child < heapSize && heap[child] < heap[child + 1])
            child++;
        if (lastElement >= heap[child])
            break;
        heap[currentNode] = heap[child];
        currentNode = child;
        child *= 2;
    }
    heap[currentNode] = lastElement;
}


template <typename T>
void maxHeap<T>::initialize(T* theHeap, int theSize) {
    delete [] heap;
    heap = theHeap;
    heapSize = theSize;

    for (int root = heapSize / 2; root >= 1; root--) {
        T rootElement = heap[root];
        int child = 2 * root;
        while (child <= heapSize) {
            if (child < heapSize && heap[child] < heap[child + 1])
                child++;
            if (rootElement >= heap[child])
                break;
            heap[child / 2] = heap[child];
            child *= 2;
        }
        heap[child / 2] = rootElement;
    }
}