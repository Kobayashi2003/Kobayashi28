#include<iostream>

using namespace std;

class two;

class one {
    private :
        int data;
    public :
        one(int data) {
            one::data = data;
        }
        ~one() {}
        void fun1() {
            cout << data << endl;
        }
        void function(two &t);
        friend class two;
};

class two {
    private :
        int data;
    public :
        two(int data) {
            two :: data = data;
        }
        ~two() {}
        void fun2() {
            cout << data << endl;
        }
        friend class one;
        void function(one &o);
};

void one::function(two &t) {
    cout << "OUT1: " << data + t.data << endl;
}

void two::function(one &o) {
    cout << "OUT2: " << data - o.data << endl;
}


int main() {
    one A(1);
    two B(2);
    A.function(B);
    B.function(A);
    return 0;
}