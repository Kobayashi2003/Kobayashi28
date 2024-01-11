#include "stack.h"
#include "chainNode.h"

template <typename T>
class linkedStack : public stack<T> {
public:
    linkedStack(int initialCapacity = 10);
    ~linkedStack();
    bool empty() const { return stackTop == nullptr; }
    int size() const { return listSize; }
    T& top() const {
        if (stackSize == 0)
            throw stackEmpty();
        return stackTop->element;
    }
    void pop(); 
    void push(const T& theElement) {
        stackTop = new chainNode<T>(theElement, stackTop);
        stackSize++;
    }
private:
    chainNode<T>* stackTop;
    int stackSize;  
};

template <typename T>
linkedStack<T>::~linkedStack() {
    while (stackTop != nullptr) {
        chainNode<T>* nextNode = stackTop->next;
        delete stackTop;
        stackTop = nextNode;
    }
}

template <typename T>
void linkedStack<T>::pop() {
    if (stackSize == 0)
        throw stackEmpty();
    
    chainNode<T>* nextNode = stackTop->next;
    delete stackTop;
    stackTop = nextNode;
    stackSize--;
} 