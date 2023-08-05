#include<iostream>

using namespace std;

class A {
    private :
        string data;
    public :
        A(string data) {
            A :: data = data;
        }
        ~A() {}
        friend int main();
};

int main() {
    A a("data");
    cout << a.data << endl;
    return 0;
}