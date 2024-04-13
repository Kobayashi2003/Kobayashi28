#include<iostream>

using namespace std;

class A {
    private :
        static int accumulator;
        int data;
    public :
        A() {
            data = 0;
        }
        A(int data) {
            A :: data = data;
            accumulator += data;
        }
        ~A() {}
        void showData() {
            cout << "Data: " << data << endl;
        }
        static void showSum() {
            cout << "Sum: " << accumulator << endl;
        }
};

int A :: accumulator = 0;

int main() {
    A a1(12);
    A a2(56);
    a1.showData();
    A :: showSum();
    return 0;
}