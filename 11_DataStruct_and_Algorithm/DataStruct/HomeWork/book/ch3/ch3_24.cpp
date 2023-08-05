// two stack in one array

#include <iostream>
// #include <stack>

using namespace std;

template <typename Object>
class TwoStack {
public:
    TwoStack(int size) : array(new Object[size]), top1(-1), top2(size), arraySize(size) {}
    ~TwoStack() { delete [] array; }

    bool isEmpty(int stackNum) const {
        if (stackNum == 1) return top1 == -1;
        else if (stackNum == 2) return top2 == arraySize;
        else {
            cout << "stackNum error!" << endl;
            return false;
        }
    }

    void push(int stackNum, const Object &x) {
        if (top1 + 1 == top2) {
            cout << "stack is full!" << endl;
            return;
        }

        if (stackNum == 1) array[++top1] = x;
        else if (stackNum == 2) array[--top2] = x;
        else {
            cout << "stackNum error!" << endl;
            return;
        }
    }

    Object pop(int stackNum) {
        if (isEmpty(stackNum)) {
            cout << "stack is empty!" << endl;
            return 0;
        }

        if (stackNum == 1) return array[top1--];
        else if (stackNum == 2) return array[top2++];
        else {
            cout << "stackNum error!" << endl;
            return 0;
        }
    }

    Object top(int stackNum) const {
        if (isEmpty(stackNum)) {
            cout << "stack is empty!" << endl;
            return 0;
        }

        if (stackNum == 1) return array[top1];
        else if (stackNum == 2) return array[top2];
        else {
            cout << "stackNum error!" << endl;
            return 0;
        }
    }

private:
    Object *array;
    int top1, top2;
    int arraySize;
};


int main() {

    TwoStack<int> s(10);
    s.push(1, 0);
    s.push(1, 1);
    s.push(1, 2);
    s.push(1, 3);

    s.push(2, 4);
    s.push(2, 5);
    s.push(2, 6);
    s.push(2, 7);
    s.push(2, 8);
    s.push(2, 9);
    
    s.push(1, 10);

    while (!s.isEmpty(1)) {
        cout << s.pop(1) << " ";
    }
    cout << endl;

    while (!s.isEmpty(2)) {
        cout << s.pop(2) << " ";
    }
    cout << endl;

    return 0;
}