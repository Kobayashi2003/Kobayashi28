#include<iostream>
// #include<typeinfo>
#include<vector>
#include<set>
#include<map>
#include<string>

using namespace std;

class Class {
    /* blank */
};

void function(int num) {
    /* blank */
}

int main() {

    int i;
    cout << "int: " << typeid(i).name() << endl;

    int *pi;
    cout << "int pointer: " << typeid(pi).name() << endl;

    char c;
    cout << "int: " << typeid(c).name() << endl;

    float f;
    cout << "float: " << typeid(f).name() << endl;

    double d;
    cout << "double: " << typeid(d).name() << endl;

    long long int lli;
    cout << "long long int: " << typeid(lli).name() << endl;

    unsigned long long int ulli;
    cout << "unsigned long long int: " << typeid(ulli).name() << endl;

    cout << "class: " << typeid(Class).name() << endl;

    cout << "function: " << typeid(function).name() << endl;

    void (*pfun)(int) = function;
    cout << "pfun: " << typeid(pfun).name() << endl;

    vector <int> v;
    cout << "vector: " << typeid(v).name() << endl;

    set <int> s;
    cout << "set: " << typeid(s).name() << endl;

    map <string, int> m;
    cout << "map: " << typeid(m).name() << endl;

    string str;
    cout << "str: " << typeid(str).name() << endl;

    return 0;
}