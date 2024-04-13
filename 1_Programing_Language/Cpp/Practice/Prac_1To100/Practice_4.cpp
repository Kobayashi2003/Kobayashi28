#include<iostream>

using namespace std;

class Member1 {
    private :
        int data;
    public:
        Member1(int tData) {
            data = tData;
            cout << "Construtor of Member1 work" << endl;
        }
        ~Member1() {
            cout << "Member1 destructor work" << endl;
        }
        void out() {
            cout << "Member1: " << data << endl;
        }
};

class Member2 {
    private :
        int data;
    public :
        Member2(int tData) {
            data = tData;
            cout << "Construtor of Member2 work" << endl;
        }
        ~Member2() {
            cout << "Member2 destructor work" << endl;
        }
        void out() {
            cout << "Member2: " << data << endl;
        }
};

class Test {
    private :
        int data;
        Member1 member1;
        Member2 member2;
    public :
        Test(int , int , int);
        ~Test() {
            cout << "Destructor of Test work" << endl;
        }
        void out() {
            cout << "Test: " << data << endl;
            member1.out();
            member2.out();
        }
};

Test :: Test(int tdata, int data1, int data2) : data(tdata), member1(data1), member2(data2) {
    cout << "Constructor of Test work" << endl;
}

int main() {
    Test test(0, 7, 9);
    test.out();
    return 0;
}