#include<iostream>

using namespace std;

template <typename Type>
class Stack {
private :
    enum {MAX = 10}; // constant specific to class
    Type items[MAX]; // holds stack items
    int top; // index for top stack item
public :
    Stack() {
        cout << "Stack constructor work" << endl;
        top = 0;
    }
    ~Stack() {
        cout << "Stack destructor work" << endl;
    }
    bool isempty();
    bool isfull();
    bool push(const Type & item); // add item to stack
    bool pop(Type & item); // pop top
};

template <typename Type>
bool Stack<Type>::isempty() {
    return top == 0;
}

template <typename Type>
bool Stack<Type>::isfull() {
    return top == MAX;
}

template <typename Type>
bool Stack<Type>::push(const Type & item) {
    try {
        if (isfull()) {
            throw "the stack is full";
        }
        items[top++] = item;
        return true;
    } catch (const char *errMsg) {
        cout << errMsg << endl;
        return false;
    }
}

template <typename Type>
bool Stack<Type>::pop(Type & item) {
    if(top > 0) {
        item = items[--top];
        return true;
    } else {
        cout << "the stack is empty" << endl;
        return false;
    }
}

int main() {
    Stack <int> stack;
    stack.isempty();
    stack.push(1);
    stack.push(1);
    stack.push(1);
    stack.push(1);
    stack.push(1);
    stack.push(1);
    stack.push(1);
    stack.push(1);
    stack.push(1);
    stack.push(1);
    stack.push(1);

    return 0;
}