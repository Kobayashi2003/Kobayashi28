#include "queue.h"
#include "myExceptions.h"

template <typename T>
class arrayQueue : public queue<T> {
public:
    arrayQueue(int initialCapacity = 10);
    ~arrayQueue() { delete[] queue; }
    bool empty() const { return theFront == theBack; }
    int size() const { return (theBack - theFront + arrayLength) % arrayLength; }
    T& front() { return queue[(theFront + 1) % arrayLength]; }
    T& back() { return queue[theBack]; }
    void pop();
    void push(const T& theElement);
private:
    int theFront;
    int theBack;
    int arrayLength;
    T* queue;
};


template <typename T> 
arrayQueue<T>::arrayQueue(int initialCapacity) {
    if (initialCapacity < 1) {
        std::ostringstream s;
        s << "Initial capacity = " << initialCapacity << " Must be > 0";
        throw illegalParameterValue(s.str());
    }
    arrayLength = initialCapacity + 1;
    queue = new T[arrayLength];
    theFront = 0;
    theBack = 0;
}


template <typename T>
void arrayQueue<T>::pop() {
    if (theFront == theBack) {
        throw queueEmpty();
    }
    theFront = (theFront + 1) % arrayLength;
    queue[theFront].~T();
}


template <typename T>
void arrayQueue<T>::push(const T& theElement) {
    if ((theBack + 1) % arrayLength == theFront) {
        T* newQueue = new T[2 * arrayLength];

        int start = (theFront + 1) % arrayLength;
        if (start < 2) {
            std::copy(queue + start, queue + start + arrayLength - 1, newQueue);
        }                                       
        else {
            std::copy(queue + start, queue + arrayLength - 1, newQueue);
            std::copy(queue, queue + theBack + 1, newQueue + arrayLength - start);
        }

        theFront = 2 * arrayLength - 1;
        theBack = arrayLength - 2;
        arrayLength *= 2;
        delete[] queue;
        queue = newQueue;
    }
    theBack = (theBack + 1) % arrayLength;
    queue[theBack] = theElement;
}


template <typename T>
void arrayQueue<T>::pop() {
    if (theFront == theBack)
        throw queueEmpty();
    theFront = (theFront + 1) % arrayLength;
    queue[theFront].~T();
}