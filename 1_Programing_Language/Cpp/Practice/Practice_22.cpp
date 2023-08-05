#include<iostream>

using namespace std;

template <typename T> void Swap(T & a, T & b);

struct job {
    string name;
    double salary;
    int floor;
};

template <> void Swap<job>(job & j1, job & j2);

void Show(job &j);

int main() {
    cout.precision(2);
    cout.setf(ios::fixed, ios::floatfield);
    int i = 10, j=20;
    cout << "i, j = " << i << "," << j << endl;
    Swap(i, j);
    cout << "Now i, j = " << i << "," << j << endl;

    job sue = {"Susan Yaffee", 73000.60, 7};
    job sidney = {"Sidney Taffee", 78060.72, 9};
    cout << "Before job swapping: " << endl;
    Show(sue);
    Show(sidney);
    // cin.get();
    return 0;
}

template <typename T> void Swap(T &a, T &b) {
    T temp = a;
    a = b;
    b = temp;
}

template <> void Swap<job>(job &j1, job &j2) {
    double t1;
    int t2;
    t1 = j1.salary;
    j1.salary = j2.salary;
    j2.salary = t1;
    t2 = j1.floor;
    j1.floor = j2.floor;
    j2.floor = t2;
}

void Show(job &j) {
    cout << j.name << ": $" << j.salary << " on floor" << j. floor << endl;
}