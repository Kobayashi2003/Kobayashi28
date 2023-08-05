#include<iostream>

using namespace std;

class Stack {
    private :
        int *sp, *bottom;
        int size;
    public :
        Stack(int usize) {
            size = usize;
            bottom = new int [size];
            sp = bottom;
        }
        ~Stack() {
            delete [] bottom;
        }
        void push(int data) {
            if(sp >= bottom + size) {
                cerr << "Stack overflow !" << endl;
            } else {
                *sp ++ = data;
                cout << data << "is pushed !"  << endl;
            }
        }
        int pop() {
            if(sp <= bottom) {
                cerr << "Stack is Empty !" << endl;
                return 0;
            } else {
                return *--sp;
            }
        }
};

int main() {
    Stack a(10);
    a.push(1); a.push(2); a.push(3); a.push(4);
    cout << a.pop() << endl;
    return 0;
}